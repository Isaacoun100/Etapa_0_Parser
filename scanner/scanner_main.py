from scanner import tokens              # Here we import the tokens

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
                self.code = str(file.read())                # We read the contents from the file in the specified path
                self.code = self.code + ' '

            self.current_char = 0                           # The pointer is set to the beginning of the file
            self.transition_table = tokens.transition_table # We take the tokens in from the tokens class in tokens.py

        except FileNotFoundError:
            print("There was an error opening the file, please try again")
        except PermissionError:
            print("Permission denied.")
        except IOError as e:
            print(f"An I/O error occurred: {e}")

    # This function will return the next character from the code
    def DemeElSiguienteCaracter(self):
        self.state = self.transition_table.get(self.state).get(self.code[self.current_char])    # State changed to the next
        self.current_char = self.current_char + 1                                               # Moves to the next character

    # Here we close the scanning process and show the stats
    def FinalizarScanner(self):
        print (self.result)         # Prints the results of the scanning process
        self.getStats()
        self.WallOfBricks()         # We summon the all mighty ¡WALL OF BRICKS!

    # DemeToken() will return the current token that its beeing analized
    def DemeToken(self):

        # Using the getLetter funtion prints the current char that we are analyzing in a pretty format
        print(self.getLetter(self.code, self.current_char))

        # We return to the initial state
        self.state = "q130"

        # We save the char where we at        
        self.start_char = self.current_char

        # Checks if the character is an empty space (\t, \n, \s)
        if(self.code[self.current_char].isspace()):

            # If it finds a space it advances to the next position and returns 'IS_SPACE'
            self.current_char = self.current_char + 1
            print(f"REJECTED: from {self.start_char} to {self.current_char}")
            self.current_token = "IS_SPACE"
            return self.current_token

        while(True):
            
            # Sets the current state
            self.current_token  = self.transition_table.get(self.state)

            # Here we try to check if the token is an in line comment
            if(self.code[self.current_char] == '$' and self.code[self.current_char+1] == '$'):

                # It moves a space forwards
                self.current_char = self.current_char + 1

                # Loops untill it finds the end of the line and advances the reader
                while(self.code[self.current_char] != '\n'):
                    # Add one for each step untill it finds \t
                    self.current_char = self.current_char + 1

                # Returns the 'IN_LINE_COMMENT tokent
                self.current_token = "INLINE_COMMENT"
                return self.current_token

            # Here we try to check if the token is a block comment
            if(self.code[self.current_char] == '$' and self.code[self.current_char+1] == '*'):

                # We add a value to get to the next token
                self.current_char = self.current_char + 1

                # It iterates between the characters untill it finds *$
                while( self.current_char < len(self.code)):

                    # We add a value to get to the next token
                    self.current_char = self.current_char + 1
                    
                    # Checks if the end of the value is a BLOCK_COMMENT
                    if(self.code[self.current_char] == '*' and self.code[self.current_char+1] == '$'):
                        # Jumps two chars to get to the end of the block comment
                        self.current_char = self.current_char + 2

                        # Returns the token name
                        self.current_token = "BLOCK_COMMENT"
                        return self.current_token

            # Checks if the number is an accepted state (State under 130)
            numberState = int(self.state[1:])

            # Checks if the current state is on the accepted states
            if(numberState < 130): 

                # Return the accepted token state
                print(f"ACCEPTED: {self.state} from {self.start_char} to {self.current_char}")
                
                if((self.current_char - self.start_char) > 1):
                    self.current_char = self.current_char - 1

                return self.current_token
            
            else:

                # If its not an accepted state then it cycles through the states
                validChar = self.code[self.current_char]
                stateReturn = self.current_token.get(validChar)
                
                #Checks if the current state exists, this is possible because the stateReturn returns None if there is no value
                if(stateReturn):
                    self.DemeElSiguienteCaracter()
                else:

                    # Identifies an id and it sends the user to check if its a possible ID
                    if(validChar.isalpha() or validChar == '_' ):
                        self.state = "q700"
                        
                    else:
                        # If none of the previuos conditions are met then there is an error and so it returns an error token
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
        
        # This is the result code (The original is not adited)
        wall = self.code

        # The offset every time we add a new value
        adjust = 0

        # Counter
        x = 0

        #Checks all of the entries in the result array
        while(x < len(self.result)):

            # Add the line of code that changes the color, to avoid a separate list the color comes from the token name converted to hex
            openHTML = f'<span style="background-color:{self.string_to_hex_color(self.result[x][0])}">'
            wall = self.insert_string(wall, openHTML , self.result[x][1]+adjust)
            adjust = adjust + 39

            if(self.result[x][0] == "BLOCK_COMMENT"):
                for i in range(self.result[x][1]+adjust, self.result[x][2]+adjust):
                    if(wall[i] == '\n'):
                        wall = wall[:i] + f'</span>\n{openHTML}' +  wall[i+1:]
                        adjust = adjust + 7 + len(openHTML)

            wall = self.insert_string(wall, '</span>', self.result[x][2]+adjust)
            adjust = adjust + 7

            x = x + 1

        wall = "<h3>" + wall.replace('\n', "</h3>\n<h3>") + "</h3>"
        
        with open('result.html', 'w') as f:
             f.write(wall)
    
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

        # The current list
        stats = [ [self.result[0][0] , 0] ]

        print(f"El código tiene {len(self.code)} caracteres")
        print(f"Se aceptó en total {len(self.result)} tokens")


        # We iterate through the items
        for item in self.result:
            token_type = item[0]
            counter[token_type] = counter.get(token_type, 0) + 1

        # Here it prints the results
        for token_type, count in counter.items():
            print(f"{token_type} aparece {count} veces")

