from scanner import tokens

class scanner:
    def __init__(self, path):
        self.path = path                # Where the code is
        self.code = None                # The code as text
        self.result = []                # Where the tokens are stored
        self.current_char = 0           # The number of the index of the code we are checking
        self.start_char = 0
        self.current_token = None       # The object inside the state
        self.state = "q130"             # Initial State
        self.transition_table = None    # The table with all of the transitions
        #self.accepting_states = tokens.getAcceptingStates

    def InicializarScanner(self):
        try:
            with open(self.path, 'r') as file:
                self.code = str(file.read())

            self.current_char = 0
            self.transition_table = tokens.transition_table

        except FileNotFoundError:
            print("There was an error opening the file, please try again")
        except PermissionError:
            print("Permission denied.")
        except IOError as e:
            print(f"An I/O error occurred: {e}")

    # This function will return the next character from the code
    def DemeElSiguienteCaracter(self):
        self.state = self.transition_table.get(self.state).get(self.code[self.current_char])
        self.current_char = self.current_char + 1

    # Here we close the scanning process and show the stats
    def FinalizarScanner(self):
        print (self.result)

    # DemeToken() will return the current token that its beeing analized
    def DemeToken(self):

        print(self.getLetter(self.code, self.current_char))

        self.state = "q130"

        self.start_char = self.current_char

        if(self.code[self.current_char].isspace()):
            self.current_char = self.current_char + 1
            print(f"REJECTED: from {self.start_char} to {self.current_char}")
            return "IS_SPACE"

        while(True):
            
            self.current_token  = self.transition_table.get(self.state)
            
            numberState = int(self.state[1:])

            if(numberState < 130): # Checks if the current state is on the accepted states

                print(f"ACCEPTED: {self.state} from {self.start_char} to {self.current_char}")
                self.current_char = self.current_char - 1

                return self.current_token
            
            else:

                validChar = self.code[self.current_char]
                stateReturn = self.current_token.get(validChar)
                
                if(stateReturn):
                    self.DemeElSiguienteCaracter()
                else:

                    if(validChar.isalpha() or validChar == '_' ):
                        self.state = "q700"
                        
                    else:
                        self.current_char = self.current_char + 1
                        print(f"ERROR: {self.state} from {self.start_char} to {self.current_char}")
                        self.current_token = "ERROR_TOKEN"
                        return self.current_token




    # If the user accepts the token then we will be adding it to the result
    def TomeToken(self):
        self.result.append( [self.current_token, self.start_char, self.current_char] )


    def getLetter(self, text, letter_index):
        # Normalize all newlines to '\n'
        normalized_text = text.replace('\r\n', '\n').replace('\r', '\n')

        if letter_index < 0 or letter_index >= len(normalized_text):
            return "Invalid index."

        # Split into lines
        lines = normalized_text.split('\n')

        # Find which line contains the letter
        count = 0
        for i, line in enumerate(lines):
            if count + len(line) >= letter_index:
                local_index = letter_index - count
                # Make sure local_index is within line length
                if local_index >= len(line):
                    return f"Line {i+1}: (letter is a newline or outside the line)"
                highlighted_line = (
                    line[:local_index] + "[" + line[local_index] + "]" + line[local_index+1:]
                )
                return f"Line {i+1}: {highlighted_line}"

            # Move past this line plus one for the '\n'
            count += len(line) + 1

        return "Letter not found in lines."

    # The wall of bricks will display the stats of the scanned code in HTML
    def WallOfBricks(self):
        return None