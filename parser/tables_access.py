import ctypes

# Cargar la librería compilada
#lib = ctypes.CDLL(r'source\c\libparser.dll')
lib = ctypes.CDLL(r'source/c/libparser.so')  # o .dll en Windows

# Definir constantes (asegúrate que coincidan con tus archivos .h)
NO_TERMINAL_INICIAL = 53
TOTAL_NO_TERMINALES = 31
MAX_LADO_DER = 12
MAX_FOLLOWS = 10

# Acceder a los arrays como punteros
TablaParsing = (ctypes.c_int * (31 * NO_TERMINAL_INICIAL)).from_address(
    ctypes.addressof(lib.TablaParsing)
)
LadosDerechos = (ctypes.c_int * (61 * MAX_LADO_DER)).from_address(
    ctypes.addressof(lib.LadosDerechos)
)
TablaFollows = (ctypes.c_int * (31 * MAX_FOLLOWS)).from_address(
    ctypes.addressof(lib.TablaFollows)
)

TablaFamilia ={
    'WORLDNAME'         : 0,
    'COLON'             : 1,
    'DASH'              : 2,
    'BEDROCK'           : 3,
    'RESOURCEPACK'      : 4,
    'INVENTORY'         : 5,
    'RECIPE'            : 6,
    'CRAFTINGTABLE'     : 7,
    'SPAWNPOINT'        : 8,
    'OBSIDIAN'          : 9,
    'STACK'             : 10,
    'RUNE'              : 11,
    'SPIDER'            : 12,
    'TORCH'             : 13,
    'GHAST'             : 14,
    'ON'                : 15,
    'OFF'               : 16,
    'SPELL'             : 17,
    'RITUAL'            : 18,
    'POLLOCRUDO'        : 19,
    'POLLOASADO'        : 20,
    'RESPAWN'           : 21,
    'CRAFT'             : 22,
    'REPEATER'          : 23,
    'TARGET'            : 24,
    'DISC'              : 25,
    'SILENCE'           : 26,
    'SPAWNER'           : 27,
    'EXHAUSTED'         : 28,
    'CREEPER'           : 29,
    'IS'                : 30,
    'ISNOT'             : 31,
    'AND'               : 32,
    'OR'                : 33,
    'XOR'               : 34,
    'NOT'               : 35,
    'QUOTES'            : 36,
    'MORETHAN'          : 37,
    'MOREEQUAL'         : 38,
    'LESSTHAN'          : 39,
    'LESSEQUAL'         : 40,
    'ASSIGN'            : 41,
    'COMMA'             : 42,
    'SEMICOLON'         : 43,
    'ARROW'             : 44,
    'PARENTHESIS'       : 45,
    'WORLDSAVE'         : 46,
    'IDENTIFIER'        : 47,
    'STRING'            : 48,
    'CHAR'              : 49,
    'FLOAT'             : 50,
    'INTEGER'           : 51,
    'EOF'               : 52
}