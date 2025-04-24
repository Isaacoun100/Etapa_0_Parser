from scanner import tokens

class scanner:
    def __init__(self, path):
        self.path = path
        self.code = None
        self.result = []
        self.current_char = None
        self.current_token = None
        self.state = 0
        self.transition_table = tokens.transition_table

    def InicializarScanner(self):
        try:
            with open(self.path, 'r') as file:
                self.code = file.read()
        except FileNotFoundError:
            print("There was an error opening the file, please try again")
        except PermissionError:
            print("Permission denied.")
        except IOError as e:
            print(f"An I/O error occurred: {e}")

    def DemeElSiguienteCaracter(self):
        return None

    def TomeEsteCaracter(self):
        return None

    def FinalizarScanner(self, result):
        return None

    def DemeToken():
        return None

    def TomeToken():
        return None

    def WallOfBricks(self, result):
        return None