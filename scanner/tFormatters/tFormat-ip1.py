import re
from typing import Dict

def shift_states(states: Dict[str, Dict[str, str]],
                 stateInc: int = 1
                ) -> Dict[str, Dict[str, str]]:
    """
    Dado un diccionario de la forma {'qN': {simbolo: 'qM', ...}, ...}
    devuelve un nuevo diccionario con todos los índices N y M sumados por stateInc.
    """
    def shift_label(label: str) -> str:
        # Solo transformamos labels que empiecen por 'q' seguido de dígitos
        m = re.fullmatch(r'(q)(\d+)', label)
        if not m:
            return label
        prefix, num = m.groups()
        new_num = int(num) + stateInc
        # Conserva el ancho original con ceros a la izquierda
        return f"{prefix}{new_num:0{len(num)}d}"

    new_states: Dict[str, Dict[str, str]] = {}
    for old_state, trans in states.items():
        new_state = shift_label(old_state)
        new_transitions: Dict[str, str] = {}
        for sym, tgt in trans.items():
            new_transitions[sym] = shift_label(tgt)
        new_states[new_state] = new_transitions

    return new_states


if __name__ == "__main__":
    data = {
        'q216': {'I': 'q217', 'i': 'q217'},
        'q217': {'N': 'q218', 'n': 'q218'},
        'q218': {'V': 'q219', 'v': 'q219'},
        'q219': {'E': 'q220', 'e': 'q220'},
        'q220': {'N': 'q221', 'n': 'q221'},
        'q221': {'T': 'q222', 't': 'q222'},
        'q222': {'O': 'q223', 'o': 'q223'},
        'q223': {'R': 'q224', 'r': 'q224'},
        'q224': {'Y': 'q03', 'y': 'q03'},
        'q225': {'R': 'q226', 'r': 'q226'},
        'q226': {'E': 'q227', 'e': 'q227'},
        'q227': {'C': 'q228', 'c': 'q228'},
        'q228': {'I': 'q229', 'i': 'q229'},
        'q229': {'P': 'q230', 'p': 'q230'},
        'q230': {'E': 'q04', 'e': 'q04'},
    }

    # Ejemplo: sumar 3 a todos los índices
    shifted = shift_states(data, stateInc=2)
    import pprint
    pprint.pprint(shifted)
