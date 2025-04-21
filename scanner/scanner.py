from tokens import TOKEN_REGEX, Token

class Scanner:
    def __init__(self, filepath):
        self.filepath = filepath # This is the file for the file that will be scanned
        self.buffer = '' # Contents of the buffer to be scanned
        self.index = 0 # This is the index of the current character in the buffer
        self.line = 1 # This is the current line number in the buffer
        self.current_token = None # This is the current token being scanned (Note, we use None because that the default result from the match function)
        self.errors =  [] # Here we will save the error from the code

        