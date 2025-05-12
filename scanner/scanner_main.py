from scanner import tokens              # Here we import the tokens


# Scanner version 1.1
# Changelog: The previous scanner didn't quite follow the structure to implement
# the parser, so we modified the logic of the scanner to it follows what the methos
# DemeToken, TomeToken, DemeCaracter and TomeCaracter has to do according to the theory
# that way we can implement the pseudocode provided.
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


    # This fuction is used to initialize the class, it opens the file and it assings it to the self.code
    def InicializarScanner(self):
        try:
            with open(self.path, 'r') as file:
                # We read the contents from the file in the specified path
                self.code = file.read() + ' '

            # The pointer is set to the beginning of the file
            self.current_char = 0
            # We take the tokens in from the tokens class in tokens.py
            self.transition_table = tokens.transition_table

        # Error management
        except FileNotFoundError:
            print("There was an error opening the file, please try again")
        except PermissionError:
            print("Permission denied.")
        except IOError as e:
            print(f"An I/O error occurred: {e}")

    # This function will return the next character from the code
    def DemeElSiguienteCaracter(self):
        # Checks if the next character is out of index, returns None if true
        if self.current_char >= len(self.code):
            self.state = None
            return
        char = self.code[self.current_char]
        self.state = self.transition_table.get(self.state, {}).get(char)
        self.current_char += 1

    # Jumps to the next character in the code
    def TomeEsteCaracter(self):
        self.current_char += 1

    # Here we close the scanning process and show the stats
    def FinalizarScanner(self):
        # Prints the results of the scanning process
        self.getStats()
        # We summon the all mighty ¡WALL OF BRICKS!
        self.WallOfBricks()

    # DemeToken() will return the current token that its beeing analized
    def DemeToken(self):

        # Using the getLetter funtion prints the current char that we are analyzing in a pretty format
        print(self.getLetter(self.code, self.current_char))

        # We return to the initial state
        self.state = "q130"

        # We save the char where we at 
        self.start_char = self.current_char

        # Checks if the character is an empty space (\t, \n)
        if self.es_espaciador():
            return self.current_token

        # We check if the current char is a possible comment
        if self.reconocer_comentario():
            return self.current_token


        while True:

            # Sets the current state
            self.current_token = self.transition_table.get(self.state)

            # Checks if the current state we are in is an accept state
            if (int(self.state[1:]) < 130):
                
                # Return the accepted token state
                print(f"ACCEPTED: {self.state} from {self.start_char} to {self.current_char}")
                
                if (self.current_char - self.start_char > 1):
                    # We return a position to evaluate from the start next time
                    self.current_char -= 1

                # We set the current state
                self.current_token = self.transition_table[self.state]
                return self.current_token


            # If its not an accepted state then it cycles through the states
            valid_char = self.code[self.current_char]
            state_return = self.current_token.get(valid_char)

            #Checks if the current state exists, this is possible because the stateReturn returns None if there is no value
            if (state_return):
                self.DemeElSiguienteCaracter()

            # Identifies an id and it sends the user to check if its a possible ID
            elif valid_char.isalpha() or valid_char == '_':
                self.state = "q700"
            else:
                 # If none of the previuos conditions are met then there is an error and so it returns an error token
                self.marcar_error()
                return self.current_token


    # This function checks if the character we are checking is a space
    def es_espaciador(self):
        if self.code[self.current_char].isspace():
            self.TomeEsteCaracter()
            print(f"REJECTED: from {self.start_char} to {self.current_char}")
            self.current_token = "IS_SPACE"
            return True
        return False

    # This function checks if the character we have can or may be a comment
    def reconocer_comentario(self):
        if self.code[self.current_char:self.current_char+2] == '$$':
            self.TomeEsteCaracter()
            while self.code[self.current_char] != '\n':
                self.TomeEsteCaracter()
            self.current_token = "INLINE_COMMENT"
            return True

        if self.code[self.current_char:self.current_char+2] == '$*':
            self.TomeEsteCaracter()
            while self.current_char < len(self.code):
                self.TomeEsteCaracter()
                if self.code[self.current_char:self.current_char+2] == '*$':
                    self.current_char += 2
                    self.current_token = "BLOCK_COMMENT"
                    return True
        return False


    # Print the current error found and continues with the scanning
    def marcar_error(self):
        self.TomeEsteCaracter()
        print(f"ERROR: {self.state} from {self.start_char} to {self.current_char}")
        self.current_token = "ERROR_TOKEN"
    
    # If the user accepts the token then we will be adding it to the result 
    def TomeToken(self):

        # Isolates the lexeme that we are checking
        lexema = self.code[self.start_char:self.current_char]
        token_info = {
            'familia': self.current_token,
            'lexema': lexema,
            'fila': self.get_row(self.start_char),
            'col_inicio': self.start_char,
            'col_fin': self.current_char - 1
        }
        self.result.append(token_info)

    # Returns the row that we are in at the moment of the scanning
    def get_row(self, index):
        return self.code[:index].count('\n') + 1

    # Returns the column that we are in at the moment of scanning
    def get_col(self, index):
        last_nl = self.code[:index].rfind('\n')
        return index - last_nl

    # Formats the provided token into a pretty string to more easily check what lexeme we are in
    def getLetter(self, text, letter_index):

        # Normalize all newlines to '\n'
        normalized_text = text.replace('\r\n', '\n').replace('\r', '\n')

        if letter_index < 0 or letter_index >= len(normalized_text):
            return "Invalid index."

        # Split into lines
        lines = normalized_text.split('\n')
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


    # The wall of bricks will display the stats of the scanned code in HTML format
    def WallOfBricks(self):

        # This is the result code (So the original is not edited)
        wall = self.code

        # The offset every time we add a new value
        adjust = 0

        #Checks all of the entries in the result array
        for token in self.result:

            # Add the line of code that changes the color, to avoid a separate list the color comes from the token name converted to hex
            openHTML = f'<span style="background-color:{self.string_to_hex_color(token["familia"])}">'
            wall = self.insert_string(wall, openHTML, token['col_inicio'] + adjust)
            adjust += len(openHTML)
            wall = self.insert_string(wall, '</span>', token['col_fin'] + adjust + 1)
            adjust += len('</span>')
        wall = "<h3>" + wall.replace('\n', "</h3>\n<h3>") + "</h3>"
        with open('result.html', 'w') as f:
            f.write(wall)

    # Takes the name of the familiy of tokens and it converts it into a hex color value
    def string_to_hex_color(self, s):
        # Limit to 20 characters
        s = s[:20]

        # Create a simple hash by summing ASCII values
        hash_value = sum(ord(c) for c in s)

        # Use hash to generate RGB components
        r = (hash_value * 123) % 256
        g = (hash_value * 456) % 256
        b = (hash_value * 789) % 256

        # Format as hex color
        return "#{:02X}{:02X}{:02X}".format(r, g, b)

    # Aux function to join strings
    def insert_string(self, original, to_insert, position):
        return original[:position] + to_insert + original[position:]

    #This method returns the stats for the tokens
    def getStats(self):

        # Where we store the results
        counter = {}
        
        print(f"El código tiene {len(self.code)} caracteres")
        print(f"Se aceptó en total {len(self.result)} tokens")

        # We iterate through the items
        for item in self.result:
            familia = item['familia']
            counter[familia] = counter.get(familia, 0) + 1

        # Here it prints the results
        for familia, count in counter.items():
            print(f"{familia} aparece {count} veces")