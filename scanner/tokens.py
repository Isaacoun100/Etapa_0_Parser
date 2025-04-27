transition_table

# Ejemplo con worldname y world save
100 #estado inicial

# WORLDNAME
    '100': {'W': 'q201', 'w': 'q201'},
    
    'q201': {'O': 'q202', 'o': 'q202'},
    'q202': {'R': 'q203', 'r': 'q203'},
    'q203': {'L': 'q204', 'l': 'q204'},
    'q204': {'D': 'q205', 'd': 'q205'},
    'q205': {'N': 'q206', 'n': 'q206' , 'S': 'q644', 's': 'q644'},
    'q206': {'A': 'q207', 'a': 'q207'},
    'q207': {'M': 'q208', 'm': 'q208'},
    'q208': {'E': 'q209', 'e': 'q209'},
    'q209': {' ': 'q01', '*': 'qX', ';': 'q01'},
    
#WORLDSAVE
    'q644': {'A': 'q645', 'a': 'q645'},
    'q645': {'V': 'q646', 'v': 'q646'},
    'q646': {'E': 'q647', 'e': 'q647'},
    'q647': {' ': 'q63', '*': 'qX', ';': 'q63'}

#ID
    'qX': {' ': 'qID', '*': 'qX'}
}

def getTransitionTable():
    return transition_table

print(transition_table.get('q10'))