def merge_blocks(blocks: list[dict[str, dict[str, str]]]
                 ) -> dict[str, dict[str, str]]:
    """
    Concatena secuencias de estados con:
    - placeholder 'qZZ' y marcador 'qXX'
    - reindexado para evitar solapamientos
    - reasignación de transiciones al nuevo estado final
    """
    def parse_q(q: str) -> int | None:
        if isinstance(q, str) and q.startswith("q") and q[1:].isdigit():
            return int(q[1:])
        return None

    merged: dict[str, dict[str, str]] = {}
    prev_last: int | None = None
    placeholder = "qZZ"
    marker = "qXX"

    for block in blocks:
        # 1) rango original [lo..hi] (excluimos placeholder)
        nums = [
            n for k in block
            if k != placeholder and (n := parse_q(k)) is not None
        ]
        lo, hi = min(nums), max(nums)
        # 2) cálculo de offset
        offset = 0 if prev_last is None else prev_last + 1 - lo

        # 3) desplazar estados "normales"
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
                # solo desplazar si apunta dentro de [lo..hi]
                if t is not None and lo <= t <= hi:
                    new_trans[sym] = f"q{t + offset}"
                else:
                    new_trans[sym] = tgt
            shifted[new_k] = new_trans

        # 4) detectar common_target en el estado original q{hi}
        orig_prev = block[f"q{hi}"]
        common_target = next(v for v in orig_prev.values() if v != marker)

        # 5) crear nuevo estado final y ajustar prev en shifted
        prev_state = f"q{hi + offset}"
        new_last = f"q{hi + offset + 1}"
        # reasignar en prev_state: common_target → new_last
        for sym, tgt in shifted[prev_state].items():
            if tgt == common_target:
                shifted[prev_state][sym] = new_last
        # construir transiciones de new_last a partir de placeholder
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

        # 6) anexar y actualizar prev_last
        merged.update(shifted)
        prev_last = hi + offset + 1

    return merged


if __name__ == "__main__":
    blocks = [
        {
            'q216': {'I': 'q217', 'i': 'q217'},
    'q217': {'N': 'q218', 'n': 'q218'},
    'q218': {'V': 'q219', 'v': 'q219'},
    'q219': {'E': 'q220', 'e': 'q220'},
    'q220': {'N': 'q221', 'n': 'q221'},
    'q221': {'T': 'q222', 't': 'q222'},
    'q222': {'O': 'q223', 'o': 'q223'},
    'q223': {'R': 'q224', 'r': 'q224'},
    'q224': {'Y': 'q03', 'y': 'q03'},
            'qZZ': {' ': 'qXX',  ';': 'qXX', '*': 'qX'},
        },
        {
            'q225': {'R': 'q226', 'r': 'q226'},
    'q226': {'E': 'q227', 'e': 'q227'},
    'q227': {'C': 'q228', 'c': 'q228'},
    'q228': {'I': 'q229', 'i': 'q229'},
    'q229': {'P': 'q230', 'p': 'q230'},
    'q230': {'E': 'q04', 'e': 'q04'},
            'qZZ': {' ': 'qXX',  ';': 'qXX', '*': 'qX'},
        },
    ]

    import pprint
    pprint.pprint(merge_blocks(blocks))