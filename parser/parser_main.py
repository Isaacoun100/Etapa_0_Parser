from scanner.scanner_main import scanner
from parser.tables_access import TablaParsing, LadosDerechos, TablaFamilia, NO_TERMINAL_INICIAL, MAX_LADO_DER

# Constants to find the EOF and simbolo inicial
token_EOF = 52
simbolo_inicial = 0

# Checks if the current family belongs to the TablaFamilia
def es_terminal(simbolo):
    # simbolo es un número entero
    return simbolo >= 100

# Parser LL(1)
def parse(scanner):

    # We store the current token
    TA = scanner.DemeToken()

    # The  heap is initialized
    pila = [simbolo_inicial]  

    while len(pila) > 0:

        #Checks if the token is a space and ommits it
        if TA['familia'] == "IS_SPACE":
            return

        EAP = pila.pop()

        # Checks if we are in a terminal
        if es_terminal(EAP):
            if TA['familia'] == EAP:
                TA = scanner.DemeToken()
            else:
                print(f"Error sintáctico: se esperaba {EAP} y se recibió {TA['familia']}")
                return
        else:
            indice_terminal = TablaFamilia[TA.get('familia')]

            if indice_terminal is None:
                print(f"Error: token con familia '{familia}' no está mapeado en TablaFamilia")
                return

            NUM_TERMINALES = len(TablaFamilia)  # Esto da 53

            regla = TablaParsing[EAP * NUM_TERMINALES + indice_terminal]

            if not (0 <= regla < 61):
                print(f"Regla inválida: {regla}")
                return

            
            # Checks from the right side
            for i in reversed(range(MAX_LADO_DER)):
                simbolo = LadosDerechos[regla * MAX_LADO_DER + i]
                if simbolo != -1:
                    pila.append(simbolo)

    # Returns the error code if it finds something wrong
    if TA['familia'] != token_EOF:
        print("Error: tokens restantes después del fin de la pila")
    else:
        print("Análisis sintáctico finalizado correctamente")