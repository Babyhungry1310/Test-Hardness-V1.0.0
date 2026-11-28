import json
import os
import subprocess
import sys
from pathlib import Path
import pytest
from ruamel.yaml import YAML
from tools import validate
@pytest.fixture
def repo(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    def git(*args):
        return subprocess.run(['git', *args], check=True, capture_output=True, text=True)
    git('init', '-q')
    git('config', 'user.email', 'tester@localhost')
    git('config', 'user.name', 'tester')
    source = tmp_path / validate.SOURCE
    source.parent.mkdir(parents=True)
    source.write_text('```yaml\nid: TK-1234\ncycle: CYC-08\nwrite_scope: [src/a.py, tests/test_old.py]\nconstraints: ["allow tests/test_old.py"]\nmax_loops: 2\ndone_when: ["file exists: proof.txt", "behavior works"]\n```\n', encoding='utf-8')
    (tmp_path / 'proof.txt').write_text('proof', encoding='utf-8')
    old = tmp_path / 'tests/test_old.py'
    old.parent.mkdir()
    old.write_text('x = 1\n', encoding='utf-8')
    git('add', '.')
    git('commit', '-qm', 'base')
    monkeypatch.setenv('TK_TEST_BASE', git('rev-parse', 'HEAD').stdout.strip())
    return tmp_path
def make_run(repo, **updates):
    data = {'schema': 2, 'task': 'TK-1234', 'run': 1, 'outcome': 'DONE', 'model': 'alpha', 'branch': 'task/TK-1234-R1', 'outputs': [], 'evidence': ['proof.txt'], 'done_check': ['1 → proof.txt', '2 → proof.txt'], 'loops': ['L01 | PASS'], 'deviations': {'assumptions': [], 'differences': [], 'unverified': []}, 'escalate': 'no', 'escalation': {'spec': '', 'problem': '', 'proposal': ''}, 'touched_protected': 'no', 'keywords': [], 'usage': []}
    data.update(updates)
    path = repo / '02_work/runs/TK-1234_R1_DONE.md'
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8', newline='\n') as stream:
        stream.write('---\n')
        YAML().dump(data, stream)
        stream.write('---\n')
    return path
def codes():
    commit_changes()
    return {i['code'] for i in validate.check(os.environ['TK_TEST_BASE'])}
def commit_changes():
    subprocess.run(['git', 'add', '-A'], check=True)
    subprocess.run(['git', 'commit', '-qm', 'fixture'], check=True)
def test_valid_run_and_declared_test(repo):
    make_run(repo)
    (repo / 'tests/test_old.py').write_text('x = 2\n', encoding='utf-8')
    assert codes() == set()
def test_c1_rejects_wrong_run_number(repo):
    p = make_run(repo, run=2)
    p.rename(p.with_name('TK-1234_R2_DONE.md'))
    assert 'C1' in codes()
def test_c2_checks_done_and_evidence(repo):
    make_run(repo, done_check=['1 → exists'], loops=['L01 | FAIL'], evidence=['missing.txt'])
    assert 'C2' in codes()
def test_c3_flags_outside_scope(repo):
    make_run(repo)
    (repo / 'outside.txt').write_text('x', encoding='utf-8')
    assert 'C3' in codes()
def test_e20_requires_named_test_in_constraints(repo, monkeypatch):
    make_run(repo)
    (repo / 'tests/test_other.py').write_text('old', encoding='utf-8')
    subprocess.run(['git', 'add', 'tests/test_other.py'], check=True)
    subprocess.run(['git', 'commit', '-qm', 'add old test'], check=True)
    monkeypatch.setenv('TK_TEST_BASE', subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip())
    (repo / 'tests/test_other.py').write_text('new', encoding='utf-8')
    assert 'E20' in codes()
@pytest.mark.parametrize(('worker', 'reviewer', 'expected'), [('a[1m]', 'a', 'SAME_MODEL'), ('a', 'b', None), ('unknown', 'b', 'MODEL_UNKNOWN')])
def test_same_model_and_unknown(repo, worker, reviewer, expected):
    make_run(repo, model=worker)
    p = repo / '03_output/CYC-08/checks/RVW-CYC-08.md'
    p.parent.mkdir(parents=True)
    p.write_text(f'---\nreviewer_model: {json.dumps(reviewer)}\nworker_models: [{json.dumps(worker)}]\n---\n', encoding='utf-8')
    actual = codes()
    assert (expected in actual) if expected else ('SAME_MODEL' not in actual and 'MODEL_UNKNOWN' not in actual)
def test_claim_mismatch_and_unknown_behavior(repo):
    make_run(repo, self_check=[{'done_when': 1, 'claim': 'PASS', 'evidence': 'missing.txt'}, {'done_when': 2, 'claim': 'PASS', 'evidence': 'present.txt'}])
    (repo / 'present.txt').write_text('exists', encoding='utf-8')
    commit_changes()
    issues = [x for x in validate.check(os.environ['TK_TEST_BASE']) if x['code'] == 'CLAIM_MISMATCH']
    assert len(issues) == 1 and 'done_when 1' in issues[0]['detail']
def test_absent_self_check_does_not_create_mismatch(repo):
    make_run(repo)
    assert 'CLAIM_MISMATCH' not in codes()
def test_untracked_evidence_does_not_change_head_result(repo):
    make_run(repo, evidence=['new-proof.txt'], done_check=['1 → new-proof.txt', '2 → new-proof.txt'])
    commit_changes()
    before = validate.check(os.environ['TK_TEST_BASE'])
    (repo / 'new-proof.txt').write_text('untracked', encoding='utf-8')
    assert validate.check(os.environ['TK_TEST_BASE']) == before
    assert any(i['code'] == 'C2' for i in before)
def test_descriptions_without_evidence_are_not_proof(repo):
    make_run(repo, evidence=[], done_check=['1 → exists', '2 → checked'])
    assert 'C2' in codes()
def test_prohibited_test_mention_is_not_authorization():
    assert not validate.declared_test('tests/test_old.py', ['khong duoc sua tests/test_old.py'])
    assert validate.declared_test('tests/test_old.py', ['duoc sua tests/test_old.py'])
    assert validate.declared_test('tests/test_old.py', ['được sửa tests/test_old.py'])
    assert not validate.declared_test('tests/test_old.py', ['không được sửa tests/test_old.py'])
    assert not validate.declared_test('tests/Test_old.py', ['được sửa tests/test_old.py'])
def test_claim_fail_contradicts_independent_file_existence(repo):
    make_run(repo, self_check=[{'done_when': 1, 'claim': 'FAIL', 'evidence': 'proof.txt'}])
    assert 'CLAIM_MISMATCH' in codes()
def test_dec0039_b3_model_unknown_is_not_a_failure(repo):
    p = repo / '04_control/decisions/DEC-0039_quy-tac-van-hanh.md'
    p.parent.mkdir(parents=True)
    p.write_text('- 2026-11-28 | ACTIVE\n', encoding='utf-8')
    (repo / '04_control/STATE.md').write_text('- CYC-08 | BUILD | Kaizen Đợt 1\n', encoding='utf-8')
    commit_changes()
    base = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
    make_run(repo, model='UNKNOWN')
    review = repo / '03_output/CYC-08/checks/RVW-CYC-08.md'
    review.parent.mkdir(parents=True)
    review.write_text('---\nreviewer_model: UNKNOWN\nworker_models: [UNKNOWN]\n---\n', encoding='utf-8')
    commit_changes()
    assert 'MODEL_UNKNOWN' not in {i['code'] for i in validate.check(base)}
def test_evidence_token_and_loop_status_are_exact(repo):
    make_run(repo, done_check=['1 → proof.txt', '2 → missing-proof.txt'], loops=['L01 | FAIL | detail=PASS'])
    commit_changes()
    found = [i for i in validate.check(os.environ['TK_TEST_BASE']) if i['code'] == 'C2']
    assert len(found) == 2 and any('done_when 2' in i['detail'] for i in found)
def test_tracked_uncommitted_proof_is_ignored(repo):
    make_run(repo)
    commit_changes()
    before = validate.check(os.environ['TK_TEST_BASE'])
    (repo / 'proof.txt').unlink()
    subprocess.run(['git', 'add', '-u'], check=True)
    assert validate.check(os.environ['TK_TEST_BASE']) == before
def test_wrong_run_evidence_is_out_of_scope(repo):
    make_run(repo)
    p = repo / '03_output/CYC-08/checks/TK-1234_R2_log.txt'
    p.parent.mkdir(parents=True)
    p.write_text('x', encoding='utf-8')
    assert 'C3' in codes()
@pytest.mark.parametrize(('status', 'cycle_line'), [('ACTIVE', '- CYC-09 | BUILD | Đợt 2'), ('SUPERSEDED_BY DEC-0099', '- CYC-08 | BUILD | Đợt 1')])
def test_b3_not_applied_outside_scope_or_after_supersession(repo, status, cycle_line):
    p = repo / '04_control/decisions/DEC-0039_quy-tac-van-hanh.md'
    p.parent.mkdir(parents=True)
    p.write_text(f'- 2026-11-29 | {status}\n- 2026-11-28 | ACTIVE\n', encoding='utf-8')
    (repo / '04_control/STATE.md').write_text(cycle_line + '\n', encoding='utf-8')
    commit_changes()
    base = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
    make_run(repo, model='UNKNOWN')
    review = repo / '03_output/CYC-08/checks/RVW-CYC-08.md'
    review.parent.mkdir(parents=True)
    review.write_text('---\nreviewer_model: UNKNOWN\nworker_models: [UNKNOWN]\n---\n', encoding='utf-8')
    commit_changes()
    assert 'MODEL_UNKNOWN' in {i['code'] for i in validate.check(base)}
def test_cli_modes_and_bad_base(repo):
    make_run(repo, done_check=[])
    commit_changes()
    script = Path(validate.__file__).resolve()
    default = subprocess.run([sys.executable, str(script), '--base', os.environ['TK_TEST_BASE'], '--json'], capture_output=True, text=True)
    strict = subprocess.run([sys.executable, str(script), '--base', os.environ['TK_TEST_BASE'], '--json', '--strict'], capture_output=True, text=True)
    error = subprocess.run([sys.executable, str(script), '--base', 'does-not-exist', '--json'], capture_output=True, text=True)
    assert default.returncode == 0 and json.loads(default.stdout)['status'] == 'WARN'
    assert strict.returncode == 1 and json.loads(strict.stdout)['status'] == 'WARN'
    assert error.returncode == 2 and json.loads(error.stdout)['status'] == 'ERROR'
