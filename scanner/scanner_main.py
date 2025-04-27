from scanner import tokens

class scanner:
    def __init__(self, path):
        self.path = path
        self.code = None
        self.result = []
        self.current_char = None
        self.current_token = None
        self.state = None
        self.transition_table = tokens.getTransitionTable
        self.accepting_states = tokens.getAcceptingStates

    def InicializarScanner(self):
        try:
            with open(self.path, 'r') as file:
                self.code = str(file.read())

            self.current_char = 0

        except FileNotFoundError:
            print("There was an error opening the file, please try again")
        except PermissionError:
            print("Permission denied.")
        except IOError as e:
            print(f"An I/O error occurred: {e}")

    # This function will return the next character from the code
    def DemeElSiguienteCaracter(self):
        return None

    # This function will be used if the character is or not going to be used
    def TomeEsteCaracter(self):
        return None

    # Here we close the scanning process and show the stats
    def FinalizarScanner(self, result):
        return None

    # DemeToken() will return the current token that its beeing analized
    def DemeToken(self):
        for lexeme in self.code:
            if lexeme.isspace():
                print("Is space")
            else:
                print(transition_table.get("q6"))


    # If the user accepts the token then we will be adding it to the result
    def TomeToken():
        return None

    # The wall of bricks will display the stats of the scanned code in HTML
    def WallOfBricks(self):
        return None