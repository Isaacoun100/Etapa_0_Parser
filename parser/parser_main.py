from scanner.scanner_main import scanner
from parser.tables_access import TablaParsing, LadosDerechos, TablaFamilia, NO_TERMINAL_INICIAL, MAX_LADO_DER

# Constants to find the EOF and simbolo inicial
token_EOF = 52
simbolo_inicial = 0


def es_terminal(codigo):
    if TablaFamilia.get(codigo):
        return True
    else:
        return False

# Parser LL(1)
def parse(scanner):
    TA = scanner.DemeToken()  # Token actual
    pila = [simbolo_inicial]  # Inicializa con el símbolo inicial <S>

    while len(pila) > 0:

        if TA['familia'] == "IS_SPACE":
            return

        EAP = pila.pop()

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

            regla = TablaParsing[EAP * NO_TERMINAL_INICIAL + indice_terminal]
            if regla < 0:
                print(f"Error sintáctico: no hay regla válida para ({EAP}, {TA['familia']})")
                return
            # Agregar el lado derecho de la regla a la pila (en orden inverso)
            for i in reversed(range(MAX_LADO_DER)):
                simbolo = LadosDerechos[regla * MAX_LADO_DER + i]
                if simbolo != -1:
                    pila.append(simbolo)

    if TA['familia'] != token_EOF:
        print("Error: tokens restantes después del fin de la pila")
    else:
        print("Análisis sintáctico finalizado correctamente")