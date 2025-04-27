import re
from typing import Dict


# --- First, define shift_states ---
def shift_states(
    states: Dict[str, Dict[str, str]], stateInc: int = 1
) -> Dict[str, Dict[str, str]]:
    def shift_label(label: str) -> str:
        m = re.fullmatch(r"(q)(\d+)", label)
        if not m:
            return label
        prefix, num = m.groups()
        new_num = int(num) + stateInc
        return f"{prefix}{new_num:0{len(num)}d}"

    new_states: Dict[str, Dict[str, str]] = {}
    state_items = list(states.items())
    last_state_key, last_state_transitions = state_items[-1]

    for old_state, transitions in state_items:
        new_state = shift_label(old_state)
        if old_state == last_state_key:
            # Last element: DO NOT shift the transition values
            new_transitions = dict(transitions)
        else:
            # Shift the transition values
            new_transitions = {
                char: shift_label(target) for char, target in transitions.items()
            }
        new_states[new_state] = new_transitions

    # Just add the line as is
    new_states["qZZ"] = {" ": "qXX", ";": "qXX", "*": "qX"}

    return new_states


# --- Then define merge_blocks ---
def merge_blocks(blocks: list[dict[str, dict[str, str]]]) -> dict[str, dict[str, str]]:
    def parse_q(q: str) -> int | None:
        if isinstance(q, str) and q.startswith("q") and q[1:].isdigit():
            return int(q[1:])
        return None

    merged: dict[str, dict[str, str]] = {}
    prev_last: int | None = None
    placeholder = "qZZ"
    marker = "qXX"

    for block in blocks:
        nums = [n for k in block if k != placeholder and (n := parse_q(k)) is not None]
        lo, hi = min(nums), max(nums)
        offset = 0 if prev_last is None else prev_last + 1 - lo

        shifted: dict[str, dict[str, str]] = {}
        for k, trans in block.items():
            if k == placeholder:
                continue
            n = parse_q(k)
            if n is None:
                continue
            new_k = f"q{n + offset}"
            new_trans: dict[str, str] = {}
            for sym, tgt in trans.items():
                t = parse_q(tgt)
                if t is not None and lo <= t <= hi:
                    new_trans[sym] = f"q{t + offset}"
                else:
                    new_trans[sym] = tgt
            shifted[new_k] = new_trans

        orig_prev = block[f"q{hi}"]
        common_target = next(v for v in orig_prev.values() if v != marker)

        prev_state = f"q{hi + offset}"
        new_last = f"q{hi + offset + 1}"
        for sym, tgt in shifted[prev_state].items():
            if tgt == common_target:
                shifted[prev_state][sym] = new_last

        new_trans: dict[str, str] = {}
        for sym, tgt in block[placeholder].items():
            if tgt == marker:
                new_trans[sym] = common_target
            else:
                t = parse_q(tgt)
                if t is not None and lo <= t <= hi:
                    new_trans[sym] = f"q{t + offset}"
                else:
                    new_trans[sym] = tgt
        shifted[new_last] = new_trans

        merged.update(shifted)
        prev_last = hi + offset + 1

    return merged


# --- Now only one if __name__ == "__main__" at the very end ---
if __name__ == "__main__":
    data = {
        "q574": {"W": "q575", "w": "q575"},
        "q575": {"O": "q576", "o": "q576"},
        "q576": {"R": "q577", "r": "q577"},
        "q577": {"L": "q578", "l": "q578"},
        "q578": {"D": "q579", "d": "q579"},
        "q579": {"S": "q580", "s": "q580"},
        "q580": {"A": "q581", "a": "q581"},
        "q581": {"V": "q582", "v": "q582"},
        "q582": {"E": "q63", "e": "q63"},
    }

    shifted = shift_states(data, stateInc=64)

    blocks = [
        shifted,
        {
            "q569": {"C": "q570", "c": "q570"},
            "q570": {"H": "q571", "h": "q571"},
            "q571": {"U": "q572", "u": "q572"},
            "q572": {"N": "q573", "n": "q573"},
            "q573": {"K": "q62", "k": "q62"},
            "qZZ": {" ": "qXX", ";": "qXX", "*": "qX"},
        },
    ]

    import pprint

    pprint.pprint(merge_blocks(blocks))
