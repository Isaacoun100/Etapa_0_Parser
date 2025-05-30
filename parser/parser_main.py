from parser.ParsingTable import ParsingTable
from parser.Rules import Rules
from parser.Stack import Stack
from parser.Terminals import Terminals
from parser.Buffer import Buffer

# Requirements
# Parsing table, Terminals, Buffer for the input, Stack, Definition of the rules

class parser:
    def __init__(self, result):

        tokenList = []
        for item in result:
            tokenList.append(item.get('familia'))

        # Previously known as userInput, moved to the constructor
        self.tokenList = tokenList
        
        self.ParsingTable = ParsingTable()
        self.pTable = self.ParsingTable.getTable()
        print(f"ptable: {self.pTable}")
        
        self.Rules = Rules()
        self.rules = self.Rules.getRules()
        print(f"rules: {self.rules}")
        
        
        self.Terminals = Terminals()
        self.terminals = self.Terminals.getTerminals()
        print(f"terminals: {self.terminals}")
        
        self.Buffer = Buffer()
        
        self.Stack = Stack()
        
        # [PENDING] The buffer should be initialized automatically 
        self.Buffer.load([])
        
        #Initilize the stack
        self.firstRule = self.rules[0]
        self.Stack.stack_insertion(self.firstRule)
        self.Stack.show()
        
        #init buffer
        self.Buffer.calcBufferLoads(self.tokenList)
        self.firstBufferLoad()
        
        self.loop()

    def loop(self):
        # We need to compare the first elements in the stack and buffer
        currentBElement = self.Buffer.current()
        currentStackElement = self.Stack.peek()

        print(f"\n[Loop]")
        print(f"Len: {self.Buffer.length()}")
        
        while self.Stack.size() > 0:
            print(f"Buffer current: {currentBElement}")
            print(f"Stack top: {currentStackElement}")
            
            # Check if the element on the stack is a terminal or a non terminal
            
            #If the  top is a non terminal we need to pop curr and push new rule
            if currentStackElement[0] == '<':
                # WARNING: Here we suppose that the terminal given by the user is
                # properly written and it is in the Terminals list, exceptions must be handeled properly
                
                print(f"pRule row: {self.pTable[currentStackElement]}")
                index = self.terminals.index(currentBElement)
                parsingRuleIndex = self.pTable[currentStackElement][index]
                print(f"pRule index: {parsingRuleIndex}")
                
                if parsingRuleIndex < 1: 
                    #ERROR case if there is no rule after reading a non terminal
                    print(f"Syntax Error: {currentBElement} is not supposed to be after {self.Stack.peekPopped()}")
                    break
                else:
                    parsingRule = self.rules[parsingRuleIndex]
                    print(f"pRule {parsingRule}")
                    self.nonTerminalSubsuitution(parsingRule)
                
            else:
                #if top of the stack contains a terminal, compare with the first element in the buffer
                if currentBElement == currentStackElement:
                    print("Match found!")
                    print(self.Buffer)
                    buffNext = self.Buffer.next()
                    if buffNext == None:
                        self.nextBufferLoad()
                    
                    self.Stack.pop()
                    self.Stack.show()
                    currentBElement = self.Buffer.current()
                        
                    if self.Stack.size() == 0:
                        print("\n ! The input has been parsed succesfully !")
                else:
                    #ERROR case if there is no rule after reading a terminal
                    print(f"Syntax Error: {currentBElement} is not supposed to be after {self.Stack.peekPopped()}")
                    break
                    
            currentStackElement = self.Stack.peek()
            print("\n")
    
    def nonTerminalSubsuitution (self, rulesRightSide):
        self.Stack.pop()
        print(self.Stack.show())
        self.Stack.stack_insertion(rulesRightSide)
        print(self.Stack.show())
        return
    
    def firstBufferLoad (self):
        if len(self.tokenList) == 0:
            print("There is no program to parse. Please introduce a program.")
        else:
            self.Buffer.load(self.tokenList)
        
    def nextBufferLoad (self):
        print("\n ==New Load==")
        print(f"Loads: {self.Buffer.getBufferLoads()}")
        print(f"last Load: {self.Buffer.getCurrentLoad()}")
        
        # Lets suppose there is a load program and we already checked if the program is less than eight instructions
        self.Buffer.incCurrentLoad()
        print(f"current Load: {self.Buffer.getCurrentLoad()}")
        self.tokenList = self.tokenList[8:]
        print(f"updated Us Input: {self.tokenList}")
        self.Buffer.flush()
        self.Buffer.load(self.tokenList)
        print(f"updated {self.Buffer}")