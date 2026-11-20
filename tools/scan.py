import argparse
import base64
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path

HIDDEN = {
    "\u200b",
    "\u200c",
    "\u200d",
    "\u2060",
    "\ufeff",
    "\u202a",
    "\u202b",
    "\u202c",
    "\u202d",
    "\u202e",
    "\u2066",
    "\u2067",
    "\u2068",
    "\u2069",
}
CONFUSABLES = {
    "\u0430": "a",
    "\u0435": "e",
    "\u043e": "o",
    "\u0440": "p",
    "\u0441": "c",
    "\u0443": "y",
    "\u0445": "x",
    "\u0456": "i",
    "\u0455": "s",
    "\u04bb": "h",
    "\u0458": "j",
    "\u0501": "d",
    "\u051b": "q",
    "\u051d": "w",
    "\u0410": "A",
    "\u0412": "B",
    "\u0415": "E",
    "\u041a": "K",
    "\u041c": "M",
    "\u041d": "H",
    "\u041e": "O",
    "\u0420": "P",
    "\u0421": "C",
    "\u0422": "T",
    "\u0425": "X",
    "\u0391": "A",
    "\u03b1": "a",
    "\u0392": "B",
    "\u0395": "E",
    "\u03b5": "e",
    "\u0399": "I",
    "\u03b9": "i",
    "\u039a": "K",
    "\u03ba": "k",
    "\u039c": "M",
    "\u039d": "N",
    "\u039f": "O",
    "\u03bf": "o",
    "\u03a1": "P",
    "\u03c1": "p",
    "\u03a4": "T",
    "\u03c4": "t",
    "\u03a7": "X",
    "\u03c7": "x",
    "\u03a5": "Y",
    "\u0396": "Z",
}
LIMITS = {
    "max_file_bytes",
    "max_decode_depth",
    "min_base64_length",
    "max_decode_count",
    "max_decoded_bytes",
}
LEVELS = {"ALLOW": 0, "WARN": 1, "QUARANTINE": 2, "BLOCK": 3}
LEVEL_NAME = {0: "ALLOW", 1: "WARN", 2: "QUARANTINE", 3: "BLOCK"}
NOTE_KEYS = {"note", "comment", "_comment"}
COMMENT_RE = re.compile(r"<!--(.*?)-->", re.DOTALL)
TAG_RE = re.compile(r"<\s*(/)?\s*([A-Za-z][\w:-]*)\b([^>]*)>", re.DOTALL)
HIDDEN_ATTR_RE = re.compile(r"(?:^|\s)hidden(?:\s|=|$)", re.IGNORECASE)
STYLE_RE = re.compile(r"style\s*=\s*([\"'])(.*?)\1", re.IGNORECASE | re.DOTALL)
TYPE_HIDDEN_RE = re.compile(r"type\s*=\s*([\"'])hidden\1", re.IGNORECASE)
VALUE_RE = re.compile(r"value\s*=\s*([\"'])(.*?)\1", re.IGNORECASE | re.DOTALL)
STRUCT_LEVELS = {
    "hidden_char": "QUARANTINE",
    "homoglyph": "QUARANTINE",
    "html_hidden": "QUARANTINE",
    "too_large": "QUARANTINE",
    "depth_exceeded": "QUARANTINE",
    "limit_exceeded": "QUARANTINE",
    "binary_file": "QUARANTINE",
}
B64_RE = re.compile(rb"[A-Za-z0-9+/=]{24,}")
PEM_RE = re.compile(rb"-----BEGIN [A-Z ]{0,30}-----[^-]+-----END [A-Z ]{0,30}-----")


class ScanError(Exception):
    pass


def emit(text, stream):
    data = text.encode("utf-8")
    buffer = getattr(stream, "buffer", None)
    if buffer is None:
        stream.write(data.decode("utf-8"))
        return
    buffer.write(data)
    buffer.flush()


def has_note(value):
    if isinstance(value, dict):
        for key, item in value.items():
            if key in NOTE_KEYS or has_note(item):
                return True
        return False
    if isinstance(value, list):
        return any(has_note(item) for item in value)
    return False


def as_limit(value):
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ScanError("TOOL_ERROR")
    return value


def load_rules(path):
    if not path.is_file():
        raise ScanError("TOOL_ERROR")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ScanError("TOOL_ERROR") from exc
    if not isinstance(data, dict) or has_note(data):
        raise ScanError("TOOL_ERROR")
    ruleset = data.get("ruleset")
    limits = data.get("limits")
    patterns = data.get("patterns")
    if not isinstance(ruleset, str) or not ruleset:
        raise ScanError("TOOL_ERROR")
    if not isinstance(limits, dict) or set(limits) != LIMITS or not isinstance(patterns, list):
        raise ScanError("TOOL_ERROR")
    parsed_limits = {key: as_limit(limits[key]) for key in LIMITS}
    compiled = []
    levels = dict(STRUCT_LEVELS)
    for item in patterns:
        if not isinstance(item, dict) or set(item) != {"rule", "group", "level", "pattern"}:
            raise ScanError("TOOL_ERROR")
        rule = item["rule"]
        group = item["group"]
        level = item["level"]
        pattern = item["pattern"]
        if not all(isinstance(part, str) and part for part in (rule, group, level, pattern)):
            raise ScanError("TOOL_ERROR")
        if level not in LEVELS:
            raise ScanError("TOOL_ERROR")
        try:
            regex = re.compile(pattern, re.IGNORECASE)
        except re.error as exc:
            raise ScanError("TOOL_ERROR") from exc
        compiled.append((rule, group, regex))
        levels[rule] = level
    return {
        "ruleset": ruleset,
        "limits": parsed_limits,
        "compiled": compiled,
        "levels": levels,
    }


def read_input(path):
    if not path.is_file():
        raise ScanError("TOOL_ERROR")
    try:
        return path.read_bytes()
    except OSError as exc:
        raise ScanError("TOOL_ERROR") from exc


def reason(rule, group, position, layer=0):
    return {"rule": rule, "group": group, "position": position, "layer": layer}


def limit_hit(name, position=0, layer=0):
    return reason(name, "limit", position, layer)


def is_binary_bytes(raw):
    if not raw:
        return False
    if b"\x00" in raw:
        return True
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return True
    control_chars = 0
    for char in text:
        code = ord(char)
        if code < 32 and code not in (9, 10, 13):
            control_chars += 1
    return control_chars > 0


def is_text_bytes(data):
    if not data or b"\x00" in data:
        return False
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return False
    for char in text:
        code = ord(char)
        if code in (9, 10, 13) or code >= 32:
            continue
        return False
    return True


def try_decode_b64(chunk, max_decoded_bytes):
    if len(chunk) > max_decoded_bytes and not chunk.endswith(b"="):
        return None
    if len(chunk) > max_decoded_bytes * 4 // 3 + 4:
        return None
    stripped = chunk.rstrip(b"=")
    pad_len = len(chunk) - len(stripped)
    if b"=" in stripped or pad_len > 2:
        return None
    rem = len(chunk) % 4
    if rem == 1:
        return None
    padded = chunk + (b"=" * ((4 - rem) % 4))
    try:
        return base64.b64decode(padded, validate=True)
    except (ValueError, base64.binascii.Error):
        return None


def decode_map(raw):
    text = raw.decode("utf-8", errors="surrogateescape")
    offsets = []
    cursor = 0
    for char in text:
        offsets.append(cursor)
        cursor += len(char.encode("utf-8", errors="surrogateescape"))
    return text, offsets


def is_emoji(char):
    if not char:
        return False
    code = ord(char)
    if 0x1F300 <= code <= 0x1FAFF or 0x2600 <= code <= 0x27BF or 0x1F1E6 <= code <= 0x1F1FF:
        return True
    if 0x1F3FB <= code <= 0x1F3FF:
        return True
    return unicodedata.category(char) == "So"


def neighbor_emoji(text, index, step):
    cursor = index + step
    while 0 <= cursor < len(text):
        char = text[cursor]
        code = ord(char)
        if char in {"\ufe0e", "\ufe0f"} or 0x1F3FB <= code <= 0x1F3FF:
            cursor += step
            continue
        return is_emoji(char)
    return False


def benign_zwj(text, index):
    return text[index] == "\u200d" and neighbor_emoji(text, index, -1) and neighbor_emoji(text, index, 1)


def strip_hidden(text):
    kept = []
    indexes = []
    hidden = []
    for index, char in enumerate(text):
        if index == 0 and char == "\ufeff":
            continue
        if benign_zwj(text, index):
            kept.append(char)
            indexes.append(index)
            continue
        if char in HIDDEN:
            hidden.append(index)
            continue
        kept.append(char)
        indexes.append(index)
    return "".join(kept), indexes, hidden


def is_latin_letter(char):
    if not unicodedata.category(char).startswith("L"):
        return False
    code = ord(char)
    if 0x0400 <= code <= 0x052F or 0x0370 <= code <= 0x03FF or 0x1F00 <= code <= 0x1FFF:
        return False
    return True


def find_homoglyphs(text):
    spans = []
    start = None
    for index, char in enumerate(text + "\n"):
        if unicodedata.category(char).startswith("L"):
            if start is None:
                start = index
            continue
        if start is None:
            continue
        word = text[start:index]
        has_latin = False
        has_lookalike = False
        for item in word:
            if item in CONFUSABLES:
                has_lookalike = True
            elif is_latin_letter(item):
                has_latin = True
        if has_latin and has_lookalike:
            spans.append(start)
        start = None
    return spans


def fold_text(text):
    return "".join(CONFUSABLES.get(char, char) for char in text)


def style_hidden(attrs):
    for match in STYLE_RE.finditer(attrs):
        style = match.group(2)
        if re.search(r"display\s*:\s*none", style, re.IGNORECASE):
            return True
        if re.search(r"visibility\s*:\s*hidden", style, re.IGNORECASE):
            return True
    return False


def hidden_spans(text):
    spans = []
    for match in COMMENT_RE.finditer(text):
        spans.append((match.start(1), match.end(1)))
    tags = list(TAG_RE.finditer(text))
    index = 0
    while index < len(tags):
        match = tags[index]
        if match.group(1):
            index += 1
            continue
        name = match.group(2).lower()
        attrs = match.group(3) or ""
        if name == "input" and TYPE_HIDDEN_RE.search(attrs):
            value = VALUE_RE.search(attrs)
            if value:
                spans.append((value.start(2), value.end(2)))
            index += 1
            continue
        if HIDDEN_ATTR_RE.search(attrs) or style_hidden(attrs):
            depth = 1
            cursor = index + 1
            end = len(text)
            while cursor < len(tags) and depth:
                other = tags[cursor]
                if other.group(2).lower() == name:
                    depth += -1 if other.group(1) else 1
                    if depth == 0:
                        end = other.start()
                cursor += 1
            spans.append((match.end(), end))
        index += 1
    return spans


def in_span(index, spans):
    for start, end in spans:
        if start <= index < end:
            return True
    return False


def pattern_hits(folded, indexes, offsets, compiled, spans):
    found = []
    for rule, group, regex in compiled:
        for match in regex.finditer(folded):
            start = match.start()
            if indexes is None:
                origin = start
                position = start
            else:
                if start >= len(indexes):
                    continue
                origin = indexes[start]
                position = offsets[origin]
            found.append(reason(rule, group, position))
            if in_span(origin, spans):
                found.append(reason("html_hidden", "concealment", position))
    return found


def sort_reasons(found):
    unique = {}
    for item in found:
        key = (item["position"], item["rule"], item["group"], item["layer"])
        unique[key] = item
    return [unique[key] for key in sorted(unique)]


def decide(found, levels):
    if not found:
        return "ALLOW"
    score = 0
    groups = set()
    request = False
    for item in found:
        groups.add(item["group"])
        level = levels.get(item["rule"], "QUARANTINE")
        score = max(score, LEVELS[level])
        if item["group"] == "zone3" or level == "BLOCK":
            score = 3
        if item["group"] == "dangerous_action" and level in {"QUARANTINE", "BLOCK"}:
            request = True
    if "concealment" in groups and request:
        score = 3
    if groups & {"override", "impersonation", "concealment"}:
        score = max(score, 2)
    if len(groups - {"limit"}) >= 2:
        score = max(score, 2)
    return LEVEL_NAME[score]


def payload(level, ruleset, digest, found, skipped=0):
    return {
        "level": level,
        "ruleset": ruleset,
        "sha256": digest,
        "reasons": found,
        "decoded_skipped": skipped,
    }


def collect_layer(raw, rules, layer, state):
    if not raw:
        return
    if raw.isascii():
        text = raw.decode("ascii")
        hits = pattern_hits(text, None, None, rules["compiled"], hidden_spans(text))
    else:
        text, offsets = decode_map(raw)
        stripped, indexes, hidden = strip_hidden(text)
        for index in hidden:
            state["found"].append(reason("hidden_char", "concealment", offsets[index], layer))
        for start in find_homoglyphs(stripped):
            state["found"].append(reason("homoglyph", "concealment", offsets[indexes[start]], layer))
        folded = fold_text(stripped)
        hits = pattern_hits(folded, indexes, offsets, rules["compiled"], hidden_spans(text))
    for item in hits:
        item["layer"] = layer
        state["found"].append(item)
    if state["blocked"] is not None:
        return
    if layer == 0 and decide(state["found"], rules["levels"]) == "BLOCK":
        return
    clean_for_b64 = PEM_RE.sub(b" ", raw)
    min_len = rules["limits"]["min_base64_length"]
    max_count = rules["limits"]["max_decode_count"]
    max_bytes = rules["limits"]["max_decoded_bytes"]
    max_depth = rules["limits"]["max_decode_depth"]
    for match in B64_RE.finditer(clean_for_b64):
        if state["blocked"] is not None:
            return
        chunk = match.group(0)
        if len(chunk) < min_len:
            continue
        start = match.start()
        decoded = try_decode_b64(chunk, max_bytes)
        if decoded is None:
            continue
        if state["count"] >= max_count:
            state["blocked"] = limit_hit("limit_exceeded", start, layer)
            return
        state["count"] += 1
        if state["decoded"] + len(decoded) > max_bytes:
            state["blocked"] = limit_hit("limit_exceeded", start, layer)
            return
        state["decoded"] += len(decoded)
        if not is_text_bytes(decoded):
            state["skipped"] += 1
            continue
        nxt = layer + 1
        if nxt > max_depth:
            state["blocked"] = limit_hit("depth_exceeded", start, layer)
            return
        collect_layer(decoded, rules, nxt, state)
        if state["blocked"] is not None:
            return


def scan_bytes(raw, rules):
    digest = hashlib.sha256(raw).hexdigest()
    if len(raw) > rules["limits"]["max_file_bytes"]:
        return payload("QUARANTINE", rules["ruleset"], digest, [reason("too_large", "limit", 0, 0)], 0)
    if is_binary_bytes(raw):
        return payload("QUARANTINE", rules["ruleset"], digest, [reason("binary_file", "format", 0, 0)], 0)
    state = {"found": [], "skipped": 0, "count": 0, "decoded": 0, "blocked": None}
    collect_layer(raw, rules, 0, state)
    if state["blocked"] is not None:
        return payload("QUARANTINE", rules["ruleset"], digest, [state["blocked"]], state["skipped"])
    ordered = sort_reasons(state["found"])
    return payload(decide(ordered, rules["levels"]), rules["ruleset"], digest, ordered, state["skipped"])


def default_rules():
    return Path(__file__).resolve().parent / "scan_rules.json"


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("--rules")
    parser.add_argument("--json", action="store_true")
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        code = exc.code
        return code if isinstance(code, int) else 2
    rules_path = Path(args.rules) if args.rules else default_rules()
    try:
        result = scan_bytes(read_input(Path(args.file)), load_rules(rules_path))
    except ScanError as exc:
        emit(str(exc) + "\n", sys.stderr)
        return 2
    text = json.dumps(result, ensure_ascii=True, separators=(",", ":"))
    emit(text + "\n", sys.stdout)
    return 0 if result["level"] in {"ALLOW", "WARN"} else 1


if __name__ == "__main__":
    sys.exit(main())