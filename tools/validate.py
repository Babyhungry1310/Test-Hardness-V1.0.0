import argparse
import json
import os
import re
import subprocess
import sys
import unicodedata
from pathlib import Path
from ruamel.yaml import YAML
RUN = re.compile(r'^02_work/runs/(TK-\d{4})_R([1-9]\d*)_(DONE|BLOCKED|CANCELLED)\.md$')
RVW = re.compile(r'^03_output/(CYC-\d{2})/checks/RVW-CYC-\d{2}(?:[-_].*)?\.md$')
MODEL = re.compile(r'^([a-z0-9][a-z0-9._-]*)(?:\[[^\[\]/]+\])?$')
SOURCE = '06_sources/SRC-0003_kaizen-chi-tiet-dot1.md'
yaml = YAML(typ='safe')
def git(*args, allow_missing=False):
    env = dict(os.environ, GIT_OPTIONAL_LOCKS='0')
    p = subprocess.run(['git', *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
    if p.returncode and not allow_missing:
        raise ValueError(p.stderr.decode('utf-8', 'replace').strip() or 'git failed')
    return p.stdout.decode('utf-8', 'strict') if not p.returncode else None
def blob(ref, path):
    return git('show', f'{ref}:{path}', allow_missing=True)
def record(text):
    if not text:
        return None
    parts = text.split('---', 2)
    try:
        value = yaml.load(parts[1] if len(parts) >= 3 and not parts[0].strip() else text)
    except Exception as exc:
        raise ValueError(f'invalid YAML: {exc}') from exc
    return value if isinstance(value, dict) else None
def cards(text):
    found = {}
    for block in re.findall(r'```yaml\s*\n(.*?)\n```', text or '', re.S):
        try:
            item = yaml.load(block)
        except Exception:
            continue
        if isinstance(item, dict) and re.fullmatch(r'TK-\d{4}', str(item.get('id', ''))):
            found[item['id']] = item
    return found
def changes(base):
    raw = git('diff', '--name-status', '-z', '--no-renames', base, 'HEAD', '--')
    parts = raw.split('\0')
    return [(parts[i], parts[i + 1]) for i in range(0, len(parts) - 1, 2)]
def current(path):
    return blob('HEAD', path) if exists(path) else None
def exists(path):
    p = Path(path)
    if p.is_absolute() or '..' in p.parts or '\\' in path:
        return False
    item = git('ls-tree', '-z', 'HEAD', '--', path)
    return any(row.split('\t', 1) == [row.split('\t', 1)[0], path] and row.startswith(('100644 blob ', '100755 blob ')) for row in item.split('\0') if '\t' in row)
def model_codes(value):
    if not isinstance(value, str):
        return None
    values = [v.strip() for v in value.split(',')]
    matches = [MODEL.fullmatch(v) for v in values]
    if not values or not all(matches) or any(v.lower() == 'unknown' for v in values):
        return None
    return {m.group(1) for m in matches}
def declared_test(path, constraints):
    for text in constraints or []:
        if not isinstance(text, str):
            continue
        for raw in re.split(r'[;\n]', text):
            paths = re.findall(r'[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)+', raw)
            clause = ''.join(c for c in unicodedata.normalize('NFD', raw.lower().replace('đ', 'd')) if unicodedata.category(c) != 'Mn')
            if path in paths and re.search(r'\b(?:allow|allowed|permit|permitted|may|duoc|cho phep)\b', clause) and not re.search(r'\b(?:not|no|never|forbid|khong|cam)\b', clause):
                return True
    return False
def check(base):
    git('rev-parse', '--verify', base + '^{commit}')
    diff = changes(base)
    all_cards = cards(blob(base, SOURCE))
    for path in git('ls-tree', '-r', '--name-only', base, '02_work/tasks').splitlines():
        if re.fullmatch(r'02_work/tasks/CYC-\d{2}/TK-\d{4}\.md', path):
            task_data = record(blob(base, path))
            if task_data and isinstance(task_data.get('id'), str):
                all_cards[task_data['id']] = task_data
    files = git('ls-tree', '-r', '--name-only', base, '02_work/runs', '03_output').splitlines()
    runs = []
    issues = []
    def add(code, path, detail):
        issues.append({'code': code, 'path': path, 'detail': detail})
    for status, path in diff:
        match = RUN.fullmatch(path)
        if path.startswith('02_work/runs/') and (not match or status != 'A'):
            add('C1', path, 'run must be a new correctly named file')
        if match and status == 'A':
            data = record(current(path))
            if not data:
                add('C1', path, 'invalid run record')
                continue
            runs.append((path, match, data))
    for path, match, data in runs:
        task, number, outcome = match.group(1), int(match.group(2)), match.group(3)
        previous = [(RUN.fullmatch(p), p) for p in files if RUN.fullmatch(p) and RUN.fullmatch(p).group(1) == task]
        max_run = max((int(m.group(2)) for m, _ in previous), default=0)
        if number != max_run + 1 or any(m.group(3) in ('DONE', 'CANCELLED') for m, _ in previous):
            add('C1', path, 'run number or closed task')
        if data.get('task') != task or data.get('run') != number or data.get('outcome') != outcome:
            add('C1', path, 'filename and record disagree')
        card = all_cards.get(task)
        if not card:
            add('C1', path, 'task not found in base')
            continue
        loops = data.get('loops') if isinstance(data.get('loops'), list) else []
        limit = card.get('max_loops', 3)
        old_numbers = []
        for _, old_path in previous:
            old = record(blob(base, old_path)) or {}
            for loop in old.get('loops', []):
                m = re.match(r'^L(\d{2})\s*\|', str(loop))
                if m:
                    old_numbers.append(int(m.group(1)))
        expected = max(old_numbers, default=0) + 1
        for loop in loops:
            m = re.match(r'^L(\d{2})\s*\|', str(loop))
            if not m or int(m.group(1)) != expected:
                add('C1', path, 'loop sequence is not continuous')
            expected += 1
        if not isinstance(limit, int) or len(loops) > limit:
            add('C1', path, 'loop limit exceeded')
        if len(loops) == limit and loops and all(len(str(x).split('|')) > 1 and str(x).split('|')[1].strip() == 'FAIL' for x in loops):
            if outcome != 'BLOCKED' or str(data.get('escalate')).lower() != 'yes':
                add('C2', path, 'exhausted loops must be BLOCKED and escalated')
        checks = data.get('done_check') if isinstance(data.get('done_check'), list) else []
        goals = card.get('done_when') if isinstance(card.get('done_when'), list) else []
        if outcome == 'DONE':
            if not loops or len(str(loops[-1]).split('|')) < 2 or str(loops[-1]).split('|')[1].strip() != 'PASS' or (data.get('deviations') or {}).get('unverified'):
                add('C2', path, 'DONE requires final PASS and no unverified')
            evidence_list = data.get('evidence') if isinstance(data.get('evidence'), list) else []
            for n in range(1, len(goals) + 1):
                rows = [str(x) for x in checks if re.match(rf'^\s*{n}\s*→\s*\S', str(x))]
                if not any(any(isinstance(e, str) and e in re.findall(r'(?<![A-Za-z0-9_./-])[A-Za-z0-9_][A-Za-z0-9_./-]*', row.split('→', 1)[1]) and exists(e) for e in evidence_list) for row in rows):
                    add('C2', path, f'done_when {n} lacks evidence')
            for evidence in evidence_list:
                if isinstance(evidence, str) and not exists(evidence):
                    add('C2', path, f'missing evidence {evidence}')
        for entry in data.get('self_check', []):
            if not isinstance(entry, dict):
                continue
            n, claim, evidence = entry.get('done_when'), entry.get('claim'), entry.get('evidence')
            if isinstance(n, int) and 1 <= n <= len(goals) and claim == 'PASS' and isinstance(evidence, str):
                if re.fullmatch(r'[A-Za-z0-9_][A-Za-z0-9_./ -]*', evidence) and '..' not in Path(evidence).parts and not exists(evidence):
                    add('CLAIM_MISMATCH', path, f'done_when {n}: missing {evidence}')
            if isinstance(n, int) and 1 <= n <= len(goals) and claim == 'FAIL' and isinstance(evidence, str):
                goal = str(goals[n - 1]).strip()
                if goal == 'file exists: ' + evidence and exists(evidence):
                    add('CLAIM_MISMATCH', path, f'done_when {n}: file exists {evidence}')
        scope = set(card.get('write_scope') or [])
        cycle = str(card.get('cycle', ''))
        for status, changed in diff:
            extra = changed == path or bool(status == 'A' and re.fullmatch(r'03_output/' + re.escape(cycle) + r'/checks/' + re.escape(task) + r'_R' + str(number) + r'_[^/]+', changed))
            if changed.startswith('04_control/gates/') or (changed not in scope and not extra):
                add('C3', changed, f'outside {task} write_scope')
            if status in ('M', 'D') and (changed.startswith('tests/') or '/tests/' in changed or Path(changed).name.startswith('test_')):
                if not declared_test(changed, card.get('constraints')):
                    add('E20', changed, 'existing test change not declared in constraints')
    reviews = [(p, record(current(p))) for status, p in diff if status != 'D' and RVW.match(p)]
    for path, review in reviews:
        if not review:
            continue
        cycle = RVW.match(path).group(1)
        prior = sum(bool(RVW.match(p) and RVW.match(p).group(1) == cycle) for p in files)
        if prior + sum(bool(RVW.match(p) and RVW.match(p).group(1) == cycle) for _, p in diff) > 3:
            add('C1', path, 'review limit exceeded')
        reviewer = model_codes(review.get('reviewer_model'))
        workers = [(run_path, run.get('model')) for run_path, _, run in runs]
        workers += [('worker_models', value) for value in review.get('worker_models', [])]
        exception = blob(base, '04_control/decisions/DEC-0039_quy-tac-van-hanh.md')
        state = blob(base, '04_control/STATE.md') or ''
        latest = re.search(r'^- \d{4}-\d{2}-\d{2} \| (ACTIVE|RETIRED|SUPERSEDED_BY DEC-\d{4})$', exception or '', re.M)
        exception = bool(latest and latest.group(1) == 'ACTIVE' and re.search(r'^- ' + re.escape(cycle) + r' \|[^\n]*Đợt 1', state, re.M) and not re.search(r'Đ5-C[^\n]*DONE', state))
        for run_path, value in workers:
            worker = model_codes(value)
            if not exception and reviewer and worker and reviewer & worker:
                add('SAME_MODEL', path, f'matches {run_path}')
            elif not exception and (not reviewer or not worker):
                add('MODEL_UNKNOWN', path, f'unknown model for {run_path}')
    return issues
def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument('--base', default='origin/main')
    p.add_argument('--strict', action='store_true')
    p.add_argument('--json', action='store_true')
    args = p.parse_args(argv)
    try:
        issues = check(args.base)
    except (OSError, UnicodeError, ValueError, TypeError) as exc:
        if args.json:
            print(json.dumps({'status': 'ERROR', 'error': str(exc)}, ensure_ascii=False))
        else:
            print(f'ERROR: {exc}', file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps({'status': 'WARN' if issues else 'PASS', 'issues': issues}, ensure_ascii=False))
    else:
        print('WARN' if issues else 'PASS')
        for issue in issues:
            print(f"{issue['code']}: {issue['path']}: {issue['detail']}")
    return 1 if args.strict and issues else 0
if __name__ == '__main__':
    sys.exit(main())
