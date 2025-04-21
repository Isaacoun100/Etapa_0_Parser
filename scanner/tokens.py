import re # We are going to use this library to read regular expresions, for more info https://docs.python.org/3/library/re.htm

TOKEN_TYPES = [
    ("WORLD_NAME",          r'\bWorldName\b'),          # Program title strcuture
    ("OPEN_WORLD",          r'\:'),                     # Used when opening a world, structure <WorldName>:

    # Sections  
    ("BEDROCK",             r'\bBedrock\b'),            # Represents the constants (Values that will not change)
    ("RESOURCE_PACK",       r'\bResourcePack\b'),       # Word used to define a new type
    ("INVENTORY",           r'\bInventory\b'),          # If I need to declare a variable it will be in this section
    ("RECIPE",              r'\bRecipe\b'),             # If I need to declare a fucntion it will be in this section
    ("CRAFTING_TABLE",      r'\bCraftingTable\b'),      # Here we will have the "body" of the program
    ("SpawnPoint",          r'\bSpawnPoint\b'),         # This is the "main" function of the program, where the program will start executing

    # Type declarations 
    ("OBSIDIAN",            r'\bObsidian\b'),           # To call constant we will use Obsidian with structure Obsidian <tipo> <id> <value>
    ("ANVIL",               r'\bAnvil\b'),              # To declare new variable types we will use Anvil with structure Anvil <id> -> <tipo>

    # ID types  
    ("TYPE_STACK",          r'\bStack\b'),              # Integer type we will use Stack with structure Stack <id> -> <value>
    ("TYPE_RUNE",           r'\bRune\b'),               # Character type we will use Rune with structure Rune <id> -> <value>
    ("TYPE_SPIDER",         r'\bSpider\b'),             # String type we will use Spider with structure Spider <id> -> <value>
    ("TYPE_TORCH",          r'\bTorch\b'),              # Boolean type we will use Torch with structure Torch <id> -> <value>
    ("TYPE_CHEST",          r'\bChest\b'),              # Set type we will use Chest with structure 
    ("TYPE_BOOK",           r'\bBook\b'),               # To take a text file we use Book with structure
    ("TYPE_GHAST",          r'\bGhast\b'),              # Float type will be used with Ghast with structure Ghast <id> -> <value>
    ("TYPE_SHELF",          r'\bShelf\b'),              # Array type will be used with Shelf with structure
    ("TYPE_ENTITY",         r'\bEntiy\b'),              # To declare registries we will use Entity with structure

    # Literals  
    ("TORCH_LITERALS",      r'(On\b|Off\b)'),           # Values for the Torch type
    ("GHAST_LIRERALS",      r'(-)?\d+(\.\d+)+'),        # Values for the Ghast type, we will use a float number
    ("STACK_LITERALS",      r'(-)?\d+'),                # Values for the Stack type, we will use an integer number
    ("CHEST_LITERALS_LEFT", r'{:'),                     # To open a set
    ("CHEST_LITERALS_RIGHT",r':}'),                     # To close a set
    ("CHEST_LITERAL_COMA",  r','),                      # To separate the elements
    ("BOOK_LITERALS_LEFT",  r'{/'),                     # To open a text file
    ("BOOK_LITERALS_RIGHT", r'/}'),                     # To close a text file
    ("SPIDER_LITERALS",     r'\"[^\"]*\"'),             # Values for the Spider type, we will use a string with double quotes
    ("SHELF_LITERALS_LEFT", r'\['),                     # To open an array
    ("SHELF_LITERALS_RIGHT",r'\]'),                     # To close an array
    ("ENTITY_LIT_LEFT",     r'{'),                      # To open a registry
    ("ENTITY_LIT_RIGHT",    r'}'),                      # To close a registry
    ("ASSIGN",              r'->'),                     # To asign a value to a variable we will use -> with structure <id> -> <value>

    # Access system: Refers to the way that we access the variables
    ("SHELF_ACCESS",   r'(\[\d\])+'),                   # For example [1, 2, 3, 4, 5]
    ("SPIDER_ACCESS",  r'[_a-zA-Z]\w*\[\d\]'),          # For example Value[2]
    ("ENTITY_ACCESS",  r'[_a-zA-Z]\w*\@[_a-zA-Z]\w*'),  # For exmple registro@Value

    # Family asignation
    ("FAMILY_SUM",          r'=\+'),                    # To sum two values we will use =+
    ("FAMILY_SUB",          r'=-'),                     # To subtract two values we will use =-
    ("FAMILY_MUL",          r'=\*'),                    # To multiply two values we will use =*
    ("FAMILY_DIV",          r'=\/'),                    # To divide two values we will use =/
    ("FAMILY_REM",          r'=%'),                     # To get the remainder of two values we will use =%


    # Increment and decrement
    ("SOULSAND",            r'\bsoulsand\b'),           # To increment a value we will use soulsand
    ("MAGMA",               r'\bmagma\b'),              # To decrement a value we will use magma

    # Basic operations: isEngraved, isInscribed, etchUp, etchDown, and, or, not, xor

    ("IS_ENGRAVED",         r'\bisEngraved(\?)?\b'),    # Checks if the character is in the alphabet
    ("IS_INSCRIBED",        r'\bisInscribed(\?)?\b'),   # Checks if the character is a digit
    ("ETCH_UP",             r'\betchUp\b'),             # Checks if the character is upper case
    ("ETCH_DOWN",           r'\betchDown\b'),           # Checks if the character is lower case
    
    # Logical operations: and, or, not, xor
    ("AND",                 r'\band\b'),                # Logical operation to check if two conditions are true
    ("OR",                  r'\bor\b'),                 # Logical operation to check if at least one condition is true
    ("NOT",                 r'\bnot\b'),                # Logical operation to negate a condition
    ("XOR",                 r'\bxor\b'),                # Logical operation to check if exactly one condition is true
    
    # String operations: bind(concat), #(length), from  ##(cut), except  ##(extract), seek(search)
    ("BIND",                r'\bbind\b'),               # String operation to concatenate two strings
    ("LENGTH",              r'\b#\b'),                  # String operation to get the length of a string
    ("FROM",                r'\bfrom\b'),               # String operation to cut a string
    ("OP",                  r'\b##\b'),                 # Instruction to cut a string
    ("EXCEPT",              r'\bexcept\b'),             # String operation to extract a substring from a string 
    ("SEARCH",              r'\bseek\b'),               # String operation to search for a substring in a string

    #Set operations: add(add), drop(delete), items(join), feed(intersect), map(belongs), biom(subset), kill(empty)
    ("ADD",                 r'\badd\b'),                # Set operation to add an element to a set
    ("DROP",                r'\bdrop\b'),               # Set operation to remove an element from a set
    ("ITEMS",               r'\bitems\b'),              # Set operation to join two sets
    ("FEED",                r'\bfeed\b'),               # Set operation to intersect two sets
    ("MAP",                 r'\bmap\b'),                # Set operation to check if an element belongs to a set
    ("BIOM",                r'\bbiom\b'),               # Set operation to check if a set is a subset of another set (Ask the teacher)
    ("KILL",                r'\bkill\b'),               # Set operation to empty a set

    # File operations: unlock(open), lock(close), craft(create), gather(read), forge(write), expand(join)
    ("UNLOCK",              r'\bunlock\b'),             # When opening a file
    ("LOCK",                r'\block\b'),               # When closing a file
    ("CRAFT",               r'\bcraft\b'),              # When creating a file
    ("GATHER",              r'\bgather\b'),             # When reading a file
    ("FORGE",               r'\bforge\b'),              # When writing to a file
    ("EXPAND",              r'\bexpand\b'),             # When joining files

    # FLoat operations :+, :-, :*, :%, ://
    ("FLOAT_ADD",          r':\+'),                     # To sum two float numbers we will use :+
    ("FLOAT_SUB",          r':-'),                      # To subtract two float numbers we will use :-
    ("FLOAT_MUL",          r':\*'),                     # To multiply two float numbers we will use :*
    ("FLOAT_REM",          r':%'),                      # To get the remainder of two float numbers we will use :%
    ("FLOAT_DIV",          r'://'),                     # To divide two float numbers we will use ://
    
    # Instruction block: PolloCrudo, PolloAsado
    ("POLLO_CRUDO",         r'\bPolloCrudo\b'),         # To open a multiline block
    ("POLLO_ASADO",         r'\bPolloAsado\b'),         # To close a multiline block

    # Instructions: repeater <cond> craft <instruction> (while), target <cond> craft hit <inst> miss <inst> (if-then-else)
    # jukebox <condition> craft , disc <case> : , silence (switch), spawner   <instrucciones> exhausted <cond> ; (Repeat until)
    # walk VAR <exp> to <exp> step <exp> craft <instrucción> (For), wither <Referencia a Record> craft <instrucción> (With)
    # creeper (break), enderPearl(continue), ragequit(Halt)

    ("REPEATER",            r'\brepeater\b'),           # Represents the while instruction
    ("CRAFT",               r'\bcraft\b'),              # General instruction for the program
    ("TARGET",              r'\btarget\b'),             # Represents the if instruction
    ("HIT",                 r'\bhit\b'),                # Represents the then instruction
    ("MISS",                r'\bmiss\b'),               # Represents the else instruction
    ("JUKEBOX",             r'\bjukebox\b'),            # Represents the switch instruction
    ("DISC",                r'\bdisc\b'),               # Represents the case instruction
    ("SILENCE",             r'\bsilence\b'),            # Represents the default instruction
    ("SPAWNER",             r'\bspawner\b'),            # Represents the repeat until instruction
    ("EXHAUSTED",           r'\bexhausted\b'),          # Instruction for the repeat until
    ("WALK",                r'\bwalk\b'),               # Represents the for instruction 
    ("TO",                  r'\bto\b'),                 # Instruction for the for
    ("STEP",                r'\bstep\b'),               # How much are we going to step
    ("WITHER",              r'\bwither\b'),             # Instruction for the record
    ("CREEPER",             r'\bcreeper\b'),            # Represents the break instruction
    ("ENDER_PEARL",         r'\benderPearl\b'),         # Represents the continue instruction
    ("RAGEQUIT",            r'\bragequit\b'),           # Represents the halt instruction

    # Headers: Spell(Function), Ritual(Procedure)
    ("SPELL",               r'\bSpell\b'),              # To declare functions 
    ("RITUAL",              r'\bRitual\b'),             # To declare procedures

    # Formal parameters: ( <type> :: <name>, <name>;  <type> ref <name>;  … )
    ("PARAM_LEFT",          r'\('),                     # The left bracet for a formal param
    ("PARAM_RIGHT",         r'\)'),                     # The right bracet for a formal param
    ("REF_PARAM",           r'\:\:'),                   # When we have type declarations we use ::

    # Instructions
    ("RESPAWN",             r'\brespawn\b'),            # When we need to return as part of a function
    ("CHUNK",               r'\bchunk\b'),              # Size of operation

    # Type cohertion
    ("TYPE_COHERTION",      r'>>'),                     # To convert a type to another type we will use >> with structure <id> >> <tipo>

    # Standart Input
    ("HOPPER_STACK",        r'\bhopperStack\b'),        # It requests an integer(stack) value from the user
    ("HOPPER_RUNE",         r'\bhopperRune\b'),         # It requests a character(rune) value from the user
    ("HOPPER_SPIDER",       r'\bhopperSpider\b'),       # It requests a string(spider) value from the user
    ("HOPPER_TORCH",        r'\bhopperTorch\b'),        # It requests a boolean(torch) value from the user
    ("HOPPER_GHAST",        r'\bhopperGhast\b'),        # It requests a float(ghast) value from the user
    ("HOPPER_CHEST",        r'\bhopperChest\b'),        # It requests a set(chest) value from the user
    ("HOPPER_BOOK",         r'\bhopperBook\b'),         # It requests a text(book) value from the user
    ("HOPPER_SHELF",        r'\bhopperShelf\b'),        # It requests an array(shelf) value from the user

    # Standart Output"
    ("DROPPER_STACK",       r'\bdropperStack\b'),       # It prints an integer(stack) value to the user
    ("DROPPER_RUNE",        r'\bdropperRune\b'),        # It prints a character(rune) value to the user
    ("DROPPER_SPIDER",      r'\bdropperSpider\b'),      # It prints a string(spider) value to the user
    ("DROPPER_TORCH",       r'\bdropperTorch\b'),       # It prints a boolean(torch) value to the user
    ("DROPPER_GHAST",       r'\bdropperGhast\b'),       # It prints a float(ghast) value to the user
    ("DROPPER_CHEST",       r'\bdropperChest\b'),       # It prints a set(chest) value to the user
    ("DROPPER_BOOK",        r'\bdropperBook\b'),        # It prints a text(book) value to the user
    ("DROPPER_SHELF",       r'\bdropperShelf\b'),       # It prints an array(shelf) value to the user

    # End of line
    ("END_LINE",            r';'),                      # To end a line we will use ;

    # End of program
    ("WORLD_SAVE",          r'\bworldSave\b'),          # To end a program we will use End with structure worldSave

    #Comments
    ("LINE_COMMENT",        r'$$\w*'),                  # To add a comment we will use $$ with structure $$ <comment>
    ("BLOCK_COMMENT",       r'$\*\w\*$'),               # To add a comment we will use $* with structure $* <comment> $*

    # Identifiers
    ("ID",                  r'[_a-zA-Z]\w*'),           # Any ID that was created previously
]


# We are converting the TOKEN_TYPES into a regular expression object (https://docs.python.org/3/library/re.html#re-objects)
# as that is more efficient than compiling each elemnt individually according to (https://docs.python.org/3/library/re.html#functions)
TOKEN_REGEX = [ (typ, re.compile(pat)) for typ, pat in TOKEN_TYPES ]

class Token:
    def __init__(self, type_, lexeme, line):
        self.type = type_
        self.lexeme = lexeme
        self.line = line

    def __repr__(self):
        return f"Token({self.type}, '{self.lexeme}', line={self.line})"
