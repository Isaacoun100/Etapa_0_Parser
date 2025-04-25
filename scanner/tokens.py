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
    ("TYPE_ENTITY",         r'\bEntity\b'),              # To declare registries we will use Entity with structure

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
    ("ACCESS",   r'(\[\d\])+'),                   # For example [1, 2, 3, 4, 5]

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
]

Transition_table:{
    'q0': {'W': 'q1', 'w': 'q1'},
    'q1': {'O': 'q2', 'o': 'q2'},
    'q10': {'B': 'q11', 'b': 'q11'},
    'q100': {'C': 'q101', 'c': 'q101'},
    'q101': {'H': 'q102', 'h': 'q102'},
    'q102': {'E': 'q103', 'e': 'q103'},
    'q103': {'S': 'q104', 's': 'q104'},
    'q104': {'T': 'q105', 't': 'q105'},
    'q105': {'B': 'q106', 'b': 'q106'},
    'q106': {'O': 'q107', 'o': 'q107'},
    'q107': {'O': 'q108', 'o': 'q108'},
    'q108': {'K': 'q109', 'k': 'q109'},
    'q109': {'G': 'q110', 'g': 'q110'},
    'q11': {'E': 'q12', 'e': 'q12'},
    'q110': {'H': 'q111', 'h': 'q111'},
    'q111': {'A': 'q112', 'a': 'q112'},
    'q112': {'S': 'q113', 's': 'q113'},
    'q113': {'T': 'q114', 't': 'q114'},
    'q114': {'S': 'q115', 's': 'q115'},
    'q115': {'H': 'q116', 'h': 'q116'},
    'q116': {'E': 'q117', 'e': 'q117'},
    'q117': {'L': 'q118', 'l': 'q118'},
    'q118': {'F': 'q119', 'f': 'q119'},
    'q119': {'E': 'q120', 'e': 'q120'},
    'q12': {'D': 'q13', 'd': 'q13'},
    'q120': {'N': 'q121', 'n': 'q121'},
    'q121': {'T': 'q122', 't': 'q122'},
    'q122': {'I': 'q123', 'i': 'q123'},
    'q123': {'T': 'q124', 't': 'q124'},
    'q124': {'Y': 'q125', 'y': 'q125'},
    'q125': {'(': 'q126'},
    'q126': {'O': 'q127', 'o': 'q127'},
    'q127': {'N': 'q128', 'n': 'q128'},
    'q128': {'|': 'q129'},
    'q129': {'O': 'q130', 'o': 'q130'},
    'q13': {'R': 'q14', 'r': 'q14'},
    'q130': {'F': 'q131', 'f': 'q131'},
    'q131': {'F': 'q132', 'f': 'q132'},
    'q132': {')': 'q133'},
    'q133': {'(': 'q134'},
    'q134': {'-': 'q135'},
    'q135': {')': 'q136'},
    'q136': {'?': 'q137'},
    'q137': {'\\': 'q138'},
    'q138': {'D': 'q139', 'd': 'q139'},
    'q139': {'+': 'q140'},
    'q14': {'O': 'q15', 'o': 'q15'},
    'q140': {'(': 'q141'},
    'q141': {'\\': 'q142'},
    'q142': {'.': 'q143'},
    'q143': {'\\': 'q144'},
    'q144': {'D': 'q145', 'd': 'q145'},
    'q145': {'+': 'q146'},
    'q146': {')': 'q147'},
    'q147': {'+': 'q148'},
    'q148': {'(': 'q149'},
    'q149': {'-': 'q150'},
    'q15': {'C': 'q16', 'c': 'q16'},
    'q150': {')': 'q151'},
    'q151': {'?': 'q152'},
    'q152': {'\\': 'q153'},
    'q153': {'D': 'q154', 'd': 'q154'},
    'q154': {'+': 'q155'},
    'q155': {'{': 'q156'},
    'q156': {':': 'q157'},
    'q157': {':': 'q158'},
    'q158': {'}': 'q159'},
    'q159': {',': 'q160'},
    'q16': {'K': 'q17', 'k': 'q17'},
    'q160': {'{': 'q161'},
    'q161': {'/': 'q162'},
    'q162': {'/': 'q163'},
    'q163': {'}': 'q164'},
    'q164': {'\\': 'q165'},
    'q165': {'"': 'q166'},
    'q166': {'[': 'q167'},
    'q167': {'^': 'q168'},
    'q168': {'\\': 'q169'},
    'q169': {'"': 'q170'},
    'q17': {'R': 'q18', 'r': 'q18'},
    'q170': {']': 'q171'},
    'q171': {'*': 'q172'},
    'q172': {'\\': 'q173'},
    'q173': {'"': 'q174'},
    'q174': {'\\': 'q175'},
    'q175': {'[': 'q176'},
    'q176': {'\\': 'q177'},
    'q177': {']': 'q178'},
    'q178': {'{': 'q179'},
    'q179': {'}': 'q180'},
    'q18': {'E': 'q19', 'e': 'q19'},
    'q180': {'-': 'q181'},
    'q181': {'>': 'q182'},
    'q182': {'(': 'q183'},
    'q183': {'\\': 'q184'},
    'q184': {'[': 'q185'},
    'q185': {'\\': 'q186'},
    'q186': {'D': 'q187', 'd': 'q187'},
    'q187': {'\\': 'q188'},
    'q188': {']': 'q189'},
    'q189': {')': 'q190'},
    'q19': {'S': 'q20', 's': 'q20'},
    'q190': {'+': 'q191'},
    'q191': {'=': 'q192'},
    'q192': {'+': 'q193'},
    'q193': {'=': 'q194'},
    'q194': {'-': 'q195'},
    'q195': {'=': 'q196'},
    'q196': {'*': 'q197'},
    'q197': {'=': 'q198'},
    'q198': {'/': 'q199'},
    'q199': {'=': 'q200'},
    'q2': {'R': 'q3', 'r': 'q3'},
    'q20': {'O': 'q21', 'o': 'q21'},
    'q200': {'%': 'q201'},
    'q201': {'S': 'q202', 's': 'q202'},
    'q202': {'O': 'q203', 'o': 'q203'},
    'q203': {'U': 'q204', 'u': 'q204'},
    'q204': {'L': 'q205', 'l': 'q205'},
    'q205': {'S': 'q206', 's': 'q206'},
    'q206': {'A': 'q207', 'a': 'q207'},
    'q207': {'N': 'q208', 'n': 'q208'},
    'q208': {'D': 'q209', 'd': 'q209'},
    'q209': {'M': 'q210', 'm': 'q210'},
    'q21': {'U': 'q22', 'u': 'q22'},
    'q210': {'A': 'q211', 'a': 'q211'},
    'q211': {'G': 'q212', 'g': 'q212'},
    'q212': {'M': 'q213', 'm': 'q213'},
    'q213': {'A': 'q214', 'a': 'q214'},
    'q214': {'I': 'q215', 'i': 'q215'},
    'q215': {'S': 'q216', 's': 'q216'},
    'q216': {'E': 'q217', 'e': 'q217'},
    'q217': {'N': 'q218', 'n': 'q218'},
    'q218': {'G': 'q219', 'g': 'q219'},
    'q219': {'R': 'q220', 'r': 'q220'},
    'q22': {'R': 'q23', 'r': 'q23'},
    'q220': {'A': 'q221', 'a': 'q221'},
    'q221': {'V': 'q222', 'v': 'q222'},
    'q222': {'E': 'q223', 'e': 'q223'},
    'q223': {'D': 'q224', 'd': 'q224'},
    'q224': {'(': 'q225'},
    'q225': {'\\': 'q226'},
    'q226': {'?': 'q227'},
    'q227': {')': 'q228'},
    'q228': {'?': 'q229'},
    'q229': {'I': 'q230', 'i': 'q230'},
    'q23': {'C': 'q24', 'c': 'q24'},
    'q230': {'S': 'q231', 's': 'q231'},
    'q231': {'I': 'q232', 'i': 'q232'},
    'q232': {'N': 'q233', 'n': 'q233'},
    'q233': {'S': 'q234', 's': 'q234'},
    'q234': {'C': 'q235', 'c': 'q235'},
    'q235': {'R': 'q236', 'r': 'q236'},
    'q236': {'I': 'q237', 'i': 'q237'},
    'q237': {'B': 'q238', 'b': 'q238'},
    'q238': {'E': 'q239', 'e': 'q239'},
    'q239': {'D': 'q240', 'd': 'q240'},
    'q24': {'E': 'q25', 'e': 'q25'},
    'q240': {'(': 'q241'},
    'q241': {'\\': 'q242'},
    'q242': {'?': 'q243'},
    'q243': {')': 'q244'},
    'q244': {'?': 'q245'},
    'q245': {'E': 'q246', 'e': 'q246'},
    'q246': {'T': 'q247', 't': 'q247'},
    'q247': {'C': 'q248', 'c': 'q248'},
    'q248': {'H': 'q249', 'h': 'q249'},
    'q249': {'U': 'q250', 'u': 'q250'},
    'q25': {'P': 'q26', 'p': 'q26'},
    'q250': {'P': 'q251', 'p': 'q251'},
    'q251': {'E': 'q252', 'e': 'q252'},
    'q252': {'T': 'q253', 't': 'q253'},
    'q253': {'C': 'q254', 'c': 'q254'},
    'q254': {'H': 'q255', 'h': 'q255'},
    'q255': {'D': 'q256', 'd': 'q256'},
    'q256': {'O': 'q257', 'o': 'q257'},
    'q257': {'W': 'q258', 'w': 'q258'},
    'q258': {'N': 'q259', 'n': 'q259'},
    'q259': {'A': 'q260', 'a': 'q260'},
    'q26': {'A': 'q27', 'a': 'q27'},
    'q260': {'N': 'q261', 'n': 'q261'},
    'q261': {'D': 'q262', 'd': 'q262'},
    'q262': {'O': 'q263', 'o': 'q263'},
    'q263': {'R': 'q264', 'r': 'q264'},
    'q264': {'N': 'q265', 'n': 'q265'},
    'q265': {'O': 'q266', 'o': 'q266'},
    'q266': {'T': 'q267', 't': 'q267'},
    'q267': {'X': 'q268', 'x': 'q268'},
    'q268': {'O': 'q269', 'o': 'q269'},
    'q269': {'R': 'q270', 'r': 'q270'},
    'q27': {'C': 'q28', 'c': 'q28'},
    'q270': {'B': 'q271', 'b': 'q271'},
    'q271': {'I': 'q272', 'i': 'q272'},
    'q272': {'N': 'q273', 'n': 'q273'},
    'q273': {'D': 'q274', 'd': 'q274'},
    'q274': {'#': 'q275'},
    'q275': {'F': 'q276', 'f': 'q276'},
    'q276': {'R': 'q277', 'r': 'q277'},
    'q277': {'O': 'q278', 'o': 'q278'},
    'q278': {'M': 'q279', 'm': 'q279'},
    'q279': {'#': 'q280'},
    'q28': {'K': 'q29', 'k': 'q29'},
    'q280': {'#': 'q281'},
    'q281': {'E': 'q282', 'e': 'q282'},
    'q282': {'X': 'q283', 'x': 'q283'},
    'q283': {'C': 'q284', 'c': 'q284'},
    'q284': {'E': 'q285', 'e': 'q285'},
    'q285': {'P': 'q286', 'p': 'q286'},
    'q286': {'T': 'q287', 't': 'q287'},
    'q287': {'S': 'q288', 's': 'q288'},
    'q288': {'E': 'q289', 'e': 'q289'},
    'q289': {'E': 'q290', 'e': 'q290'},
    'q29': {'I': 'q30', 'i': 'q30'},
    'q290': {'K': 'q291', 'k': 'q291'},
    'q291': {'A': 'q292', 'a': 'q292'},
    'q292': {'D': 'q293', 'd': 'q293'},
    'q293': {'D': 'q294', 'd': 'q294'},
    'q294': {'D': 'q295', 'd': 'q295'},
    'q295': {'R': 'q296', 'r': 'q296'},
    'q296': {'O': 'q297', 'o': 'q297'},
    'q297': {'P': 'q298', 'p': 'q298'},
    'q298': {'I': 'q299', 'i': 'q299'},
    'q299': {'T': 'q300', 't': 'q300'},
    'q3': {'L': 'q4', 'l': 'q4'},
    'q30': {'N': 'q31', 'n': 'q31'},
    'q300': {'E': 'q301', 'e': 'q301'},
    'q301': {'M': 'q302', 'm': 'q302'},
    'q302': {'S': 'q303', 's': 'q303'},
    'q303': {'F': 'q304', 'f': 'q304'},
    'q304': {'E': 'q305', 'e': 'q305'},
    'q305': {'E': 'q306', 'e': 'q306'},
    'q306': {'D': 'q307', 'd': 'q307'},
    'q307': {'M': 'q308', 'm': 'q308'},
    'q308': {'A': 'q309', 'a': 'q309'},
    'q309': {'P': 'q310', 'p': 'q310'},
    'q31': {'V': 'q32', 'v': 'q32'},
    'q310': {'B': 'q311', 'b': 'q311'},
    'q311': {'I': 'q312', 'i': 'q312'},
    'q312': {'O': 'q313', 'o': 'q313'},
    'q313': {'M': 'q314', 'm': 'q314'},
    'q314': {'K': 'q315', 'k': 'q315'},
    'q315': {'I': 'q316', 'i': 'q316'},
    'q316': {'L': 'q317', 'l': 'q317'},
    'q317': {'L': 'q318', 'l': 'q318'},
    'q318': {'U': 'q319', 'u': 'q319'},
    'q319': {'N': 'q320', 'n': 'q320'},
    'q32': {'E': 'q33', 'e': 'q33'},
    'q320': {'L': 'q321', 'l': 'q321'},
    'q321': {'O': 'q322', 'o': 'q322'},
    'q322': {'C': 'q323', 'c': 'q323'},
    'q323': {'K': 'q324', 'k': 'q324'},
    'q324': {'L': 'q325', 'l': 'q325'},
    'q325': {'O': 'q326', 'o': 'q326'},
    'q326': {'C': 'q327', 'c': 'q327'},
    'q327': {'K': 'q328', 'k': 'q328'},
    'q328': {'C': 'q329', 'c': 'q329'},
    'q329': {'R': 'q330', 'r': 'q330'},
    'q33': {'N': 'q34', 'n': 'q34'},
    'q330': {'A': 'q331', 'a': 'q331'},
    'q331': {'F': 'q332', 'f': 'q332'},
    'q332': {'T': 'q333', 't': 'q333'},
    'q333': {'G': 'q334', 'g': 'q334'},
    'q334': {'A': 'q335', 'a': 'q335'},
    'q335': {'T': 'q336', 't': 'q336'},
    'q336': {'H': 'q337', 'h': 'q337'},
    'q337': {'E': 'q338', 'e': 'q338'},
    'q338': {'R': 'q339', 'r': 'q339'},
    'q339': {'F': 'q340', 'f': 'q340'},
    'q34': {'T': 'q35', 't': 'q35'},
    'q340': {'O': 'q341', 'o': 'q341'},
    'q341': {'R': 'q342', 'r': 'q342'},
    'q342': {'G': 'q343', 'g': 'q343'},
    'q343': {'E': 'q344', 'e': 'q344'},
    'q344': {'E': 'q345', 'e': 'q345'},
    'q345': {'X': 'q346', 'x': 'q346'},
    'q346': {'P': 'q347', 'p': 'q347'},
    'q347': {'A': 'q348', 'a': 'q348'},
    'q348': {'N': 'q349', 'n': 'q349'},
    'q349': {'D': 'q350', 'd': 'q350'},
    'q35': {'O': 'q36', 'o': 'q36'},
    'q350': {':': 'q351'},
    'q351': {'+': 'q352'},
    'q352': {':': 'q353'},
    'q353': {'-': 'q354'},
    'q354': {':': 'q355'},
    'q355': {'*': 'q356'},
    'q356': {':': 'q357'},
    'q357': {'%': 'q358'},
    'q358': {':': 'q359'},
    'q359': {'/': 'q360'},
    'q36': {'R': 'q37', 'r': 'q37'},
    'q360': {'/': 'q361'},
    'q361': {'P': 'q362', 'p': 'q362'},
    'q362': {'O': 'q363', 'o': 'q363'},
    'q363': {'L': 'q364', 'l': 'q364'},
    'q364': {'L': 'q365', 'l': 'q365'},
    'q365': {'O': 'q366', 'o': 'q366'},
    'q366': {'C': 'q367', 'c': 'q367'},
    'q367': {'R': 'q368', 'r': 'q368'},
    'q368': {'U': 'q369', 'u': 'q369'},
    'q369': {'D': 'q370', 'd': 'q370'},
    'q37': {'Y': 'q38', 'y': 'q38'},
    'q370': {'O': 'q371', 'o': 'q371'},
    'q371': {'P': 'q372', 'p': 'q372'},
    'q372': {'O': 'q373', 'o': 'q373'},
    'q373': {'L': 'q374', 'l': 'q374'},
    'q374': {'L': 'q375', 'l': 'q375'},
    'q375': {'O': 'q376', 'o': 'q376'},
    'q376': {'A': 'q377', 'a': 'q377'},
    'q377': {'S': 'q378', 's': 'q378'},
    'q378': {'A': 'q379', 'a': 'q379'},
    'q379': {'D': 'q380', 'd': 'q380'},
    'q38': {'R': 'q39', 'r': 'q39'},
    'q380': {'O': 'q381', 'o': 'q381'},
    'q381': {'R': 'q382', 'r': 'q382'},
    'q382': {'E': 'q383', 'e': 'q383'},
    'q383': {'P': 'q384', 'p': 'q384'},
    'q384': {'E': 'q385', 'e': 'q385'},
    'q385': {'A': 'q386', 'a': 'q386'},
    'q386': {'T': 'q387', 't': 'q387'},
    'q387': {'E': 'q388', 'e': 'q388'},
    'q388': {'R': 'q389', 'r': 'q389'},
    'q389': {'C': 'q390', 'c': 'q390'},
    'q39': {'E': 'q40', 'e': 'q40'},
    'q390': {'R': 'q391', 'r': 'q391'},
    'q391': {'A': 'q392', 'a': 'q392'},
    'q392': {'F': 'q393', 'f': 'q393'},
    'q393': {'T': 'q394', 't': 'q394'},
    'q394': {'T': 'q395', 't': 'q395'},
    'q395': {'A': 'q396', 'a': 'q396'},
    'q396': {'R': 'q397', 'r': 'q397'},
    'q397': {'G': 'q398', 'g': 'q398'},
    'q398': {'E': 'q399', 'e': 'q399'},
    'q399': {'T': 'q400', 't': 'q400'},
    'q4': {'D': 'q5', 'd': 'q5'},
    'q40': {'C': 'q41', 'c': 'q41'},
    'q400': {'H': 'q401', 'h': 'q401'},
    'q401': {'I': 'q402', 'i': 'q402'},
    'q402': {'T': 'q403', 't': 'q403'},
    'q403': {'M': 'q404', 'm': 'q404'},
    'q404': {'I': 'q405', 'i': 'q405'},
    'q405': {'S': 'q406', 's': 'q406'},
    'q406': {'S': 'q407', 's': 'q407'},
    'q407': {'J': 'q408', 'j': 'q408'},
    'q408': {'U': 'q409', 'u': 'q409'},
    'q409': {'K': 'q410', 'k': 'q410'},
    'q41': {'I': 'q42', 'i': 'q42'},
    'q410': {'E': 'q411', 'e': 'q411'},
    'q411': {'B': 'q412', 'b': 'q412'},
    'q412': {'O': 'q413', 'o': 'q413'},
    'q413': {'X': 'q414', 'x': 'q414'},
    'q414': {'D': 'q415', 'd': 'q415'},
    'q415': {'I': 'q416', 'i': 'q416'},
    'q416': {'S': 'q417', 's': 'q417'},
    'q417': {'C': 'q418', 'c': 'q418'},
    'q418': {'S': 'q419', 's': 'q419'},
    'q419': {'I': 'q420', 'i': 'q420'},
    'q42': {'P': 'q43', 'p': 'q43'},
    'q420': {'L': 'q421', 'l': 'q421'},
    'q421': {'E': 'q422', 'e': 'q422'},
    'q422': {'N': 'q423', 'n': 'q423'},
    'q423': {'C': 'q424', 'c': 'q424'},
    'q424': {'E': 'q425', 'e': 'q425'},
    'q425': {'S': 'q426', 's': 'q426'},
    'q426': {'P': 'q427', 'p': 'q427'},
    'q427': {'A': 'q428', 'a': 'q428'},
    'q428': {'W': 'q429', 'w': 'q429'},
    'q429': {'N': 'q430', 'n': 'q430'},
    'q43': {'E': 'q44', 'e': 'q44'},
    'q430': {'E': 'q431', 'e': 'q431'},
    'q431': {'R': 'q432', 'r': 'q432'},
    'q432': {'E': 'q433', 'e': 'q433'},
    'q433': {'X': 'q434', 'x': 'q434'},
    'q434': {'H': 'q435', 'h': 'q435'},
    'q435': {'A': 'q436', 'a': 'q436'},
    'q436': {'U': 'q437', 'u': 'q437'},
    'q437': {'S': 'q438', 's': 'q438'},
    'q438': {'T': 'q439', 't': 'q439'},
    'q439': {'E': 'q440', 'e': 'q440'},
    'q44': {'C': 'q45', 'c': 'q45'},
    'q440': {'D': 'q441', 'd': 'q441'},
    'q441': {'W': 'q442', 'w': 'q442'},
    'q442': {'A': 'q443', 'a': 'q443'},
    'q443': {'L': 'q444', 'l': 'q444'},
    'q444': {'K': 'q445', 'k': 'q445'},
    'q445': {'T': 'q446', 't': 'q446'},
    'q446': {'O': 'q447', 'o': 'q447'},
    'q447': {'S': 'q448', 's': 'q448'},
    'q448': {'T': 'q449', 't': 'q449'},
    'q449': {'E': 'q450', 'e': 'q450'},
    'q45': {'R': 'q46', 'r': 'q46'},
    'q450': {'P': 'q451', 'p': 'q451'},
    'q451': {'W': 'q452', 'w': 'q452'},
    'q452': {'I': 'q453', 'i': 'q453'},
    'q453': {'T': 'q454', 't': 'q454'},
    'q454': {'H': 'q455', 'h': 'q455'},
    'q455': {'E': 'q456', 'e': 'q456'},
    'q456': {'R': 'q457', 'r': 'q457'},
    'q457': {'C': 'q458', 'c': 'q458'},
    'q458': {'R': 'q459', 'r': 'q459'},
    'q459': {'E': 'q460', 'e': 'q460'},
    'q46': {'A': 'q47', 'a': 'q47'},
    'q460': {'E': 'q461', 'e': 'q461'},
    'q461': {'P': 'q462', 'p': 'q462'},
    'q462': {'E': 'q463', 'e': 'q463'},
    'q463': {'R': 'q464', 'r': 'q464'},
    'q464': {'E': 'q465', 'e': 'q465'},
    'q465': {'N': 'q466', 'n': 'q466'},
    'q466': {'D': 'q467', 'd': 'q467'},
    'q467': {'E': 'q468', 'e': 'q468'},
    'q468': {'R': 'q469', 'r': 'q469'},
    'q469': {'P': 'q470', 'p': 'q470'},
    'q47': {'F': 'q48', 'f': 'q48'},
    'q470': {'E': 'q471', 'e': 'q471'},
    'q471': {'A': 'q472', 'a': 'q472'},
    'q472': {'R': 'q473', 'r': 'q473'},
    'q473': {'L': 'q474', 'l': 'q474'},
    'q474': {'R': 'q475', 'r': 'q475'},
    'q475': {'A': 'q476', 'a': 'q476'},
    'q476': {'G': 'q477', 'g': 'q477'},
    'q477': {'E': 'q478', 'e': 'q478'},
    'q478': {'Q': 'q479', 'q': 'q479'},
    'q479': {'U': 'q480', 'u': 'q480'},
    'q48': {'T': 'q49', 't': 'q49'},
    'q480': {'I': 'q481', 'i': 'q481'},
    'q481': {'T': 'q482', 't': 'q482'},
    'q482': {'S': 'q483', 's': 'q483'},
    'q483': {'P': 'q484', 'p': 'q484'},
    'q484': {'E': 'q485', 'e': 'q485'},
    'q485': {'L': 'q486', 'l': 'q486'},
    'q486': {'L': 'q487', 'l': 'q487'},
    'q487': {'R': 'q488', 'r': 'q488'},
    'q488': {'I': 'q489', 'i': 'q489'},
    'q489': {'T': 'q490', 't': 'q490'},
    'q49': {'I': 'q50', 'i': 'q50'},
    'q490': {'U': 'q491', 'u': 'q491'},
    'q491': {'A': 'q492', 'a': 'q492'},
    'q492': {'L': 'q493', 'l': 'q493'},
    'q493': {'(': 'q494'},
    'q494': {')': 'q495'},
    'q495': {':': 'q496'},
    'q496': {':': 'q497'},
    'q497': {'R': 'q498', 'r': 'q498'},
    'q498': {'E': 'q499', 'e': 'q499'},
    'q499': {'S': 'q500', 's': 'q500'},
    'q5': {'N': 'q6', 'n': 'q6'},
    'q50': {'N': 'q51', 'n': 'q51'},
    'q500': {'P': 'q501', 'p': 'q501'},
    'q501': {'A': 'q502', 'a': 'q502'},
    'q502': {'W': 'q503', 'w': 'q503'},
    'q503': {'N': 'q504', 'n': 'q504'},
    'q504': {'C': 'q505', 'c': 'q505'},
    'q505': {'H': 'q506', 'h': 'q506'},
    'q506': {'U': 'q507', 'u': 'q507'},
    'q507': {'N': 'q508', 'n': 'q508'},
    'q508': {'K': 'q509', 'k': 'q509'},
    'q509': {'>': 'q510'},
    'q51': {'G': 'q52', 'g': 'q52'},
    'q510': {'>': 'q511'},
    'q511': {'H': 'q512', 'h': 'q512'},
    'q512': {'O': 'q513', 'o': 'q513'},
    'q513': {'P': 'q514', 'p': 'q514'},
    'q514': {'P': 'q515', 'p': 'q515'},
    'q515': {'E': 'q516', 'e': 'q516'},
    'q516': {'R': 'q517', 'r': 'q517'},
    'q517': {'S': 'q518', 's': 'q518'},
    'q518': {'T': 'q519', 't': 'q519'},
    'q519': {'A': 'q520', 'a': 'q520'},
    'q52': {'T': 'q53', 't': 'q53'},
    'q520': {'C': 'q521', 'c': 'q521'},
    'q521': {'K': 'q522', 'k': 'q522'},
    'q522': {'H': 'q523', 'h': 'q523'},
    'q523': {'O': 'q524', 'o': 'q524'},
    'q524': {'P': 'q525', 'p': 'q525'},
    'q525': {'P': 'q526', 'p': 'q526'},
    'q526': {'E': 'q527', 'e': 'q527'},
    'q527': {'R': 'q528', 'r': 'q528'},
    'q528': {'R': 'q529', 'r': 'q529'},
    'q529': {'U': 'q530', 'u': 'q530'},
    'q53': {'A': 'q54', 'a': 'q54'},
    'q530': {'N': 'q531', 'n': 'q531'},
    'q531': {'E': 'q532', 'e': 'q532'},
    'q532': {'H': 'q533', 'h': 'q533'},
    'q533': {'O': 'q534', 'o': 'q534'},
    'q534': {'P': 'q535', 'p': 'q535'},
    'q535': {'P': 'q536', 'p': 'q536'},
    'q536': {'E': 'q537', 'e': 'q537'},
    'q537': {'R': 'q538', 'r': 'q538'},
    'q538': {'S': 'q539', 's': 'q539'},
    'q539': {'P': 'q540', 'p': 'q540'},
    'q54': {'B': 'q55', 'b': 'q55'},
    'q540': {'I': 'q541', 'i': 'q541'},
    'q541': {'D': 'q542', 'd': 'q542'},
    'q542': {'E': 'q543', 'e': 'q543'},
    'q543': {'R': 'q544', 'r': 'q544'},
    'q544': {'H': 'q545', 'h': 'q545'},
    'q545': {'O': 'q546', 'o': 'q546'},
    'q546': {'P': 'q547', 'p': 'q547'},
    'q547': {'P': 'q548', 'p': 'q548'},
    'q548': {'E': 'q549', 'e': 'q549'},
    'q549': {'R': 'q550', 'r': 'q550'},
    'q55': {'L': 'q56', 'l': 'q56'},
    'q550': {'T': 'q551', 't': 'q551'},
    'q551': {'O': 'q552', 'o': 'q552'},
    'q552': {'R': 'q553', 'r': 'q553'},
    'q553': {'C': 'q554', 'c': 'q554'},
    'q554': {'H': 'q555', 'h': 'q555'},
    'q555': {'H': 'q556', 'h': 'q556'},
    'q556': {'O': 'q557', 'o': 'q557'},
    'q557': {'P': 'q558', 'p': 'q558'},
    'q558': {'P': 'q559', 'p': 'q559'},
    'q559': {'E': 'q560', 'e': 'q560'},
    'q56': {'E': 'q57', 'e': 'q57'},
    'q560': {'R': 'q561', 'r': 'q561'},
    'q561': {'G': 'q562', 'g': 'q562'},
    'q562': {'H': 'q563', 'h': 'q563'},
    'q563': {'A': 'q564', 'a': 'q564'},
    'q564': {'S': 'q565', 's': 'q565'},
    'q565': {'T': 'q566', 't': 'q566'},
    'q566': {'H': 'q567', 'h': 'q567'},
    'q567': {'O': 'q568', 'o': 'q568'},
    'q568': {'P': 'q569', 'p': 'q569'},
    'q569': {'P': 'q570', 'p': 'q570'},
    'q57': {'S': 'q58', 's': 'q58'},
    'q570': {'E': 'q571', 'e': 'q571'},
    'q571': {'R': 'q572', 'r': 'q572'},
    'q572': {'C': 'q573', 'c': 'q573'},
    'q573': {'H': 'q574', 'h': 'q574'},
    'q574': {'E': 'q575', 'e': 'q575'},
    'q575': {'S': 'q576', 's': 'q576'},
    'q576': {'T': 'q577', 't': 'q577'},
    'q577': {'H': 'q578', 'h': 'q578'},
    'q578': {'O': 'q579', 'o': 'q579'},
    'q579': {'P': 'q580', 'p': 'q580'},
    'q58': {'P': 'q59', 'p': 'q59'},
    'q580': {'P': 'q581', 'p': 'q581'},
    'q581': {'E': 'q582', 'e': 'q582'},
    'q582': {'R': 'q583', 'r': 'q583'},
    'q583': {'B': 'q584', 'b': 'q584'},
    'q584': {'O': 'q585', 'o': 'q585'},
    'q585': {'O': 'q586', 'o': 'q586'},
    'q586': {'K': 'q587', 'k': 'q587'},
    'q587': {'H': 'q588', 'h': 'q588'},
    'q588': {'O': 'q589', 'o': 'q589'},
    'q589': {'P': 'q590', 'p': 'q590'},
    'q59': {'A': 'q60', 'a': 'q60'},
    'q590': {'P': 'q591', 'p': 'q591'},
    'q591': {'E': 'q592', 'e': 'q592'},
    'q592': {'R': 'q593', 'r': 'q593'},
    'q593': {'S': 'q594', 's': 'q594'},
    'q594': {'H': 'q595', 'h': 'q595'},
    'q595': {'E': 'q596', 'e': 'q596'},
    'q596': {'L': 'q597', 'l': 'q597'},
    'q597': {'F': 'q598', 'f': 'q598'},
    'q598': {'D': 'q599', 'd': 'q599'},
    'q599': {'R': 'q600', 'r': 'q600'},
    'q6': {'A': 'q7', 'a': 'q7'},
    'q60': {'W': 'q61', 'w': 'q61'},
    'q600': {'O': 'q601', 'o': 'q601'},
    'q601': {'P': 'q602', 'p': 'q602'},
    'q602': {'P': 'q603', 'p': 'q603'},
    'q603': {'E': 'q604', 'e': 'q604'},
    'q604': {'R': 'q605', 'r': 'q605'},
    'q605': {'S': 'q606', 's': 'q606'},
    'q606': {'T': 'q607', 't': 'q607'},
    'q607': {'A': 'q608', 'a': 'q608'},
    'q608': {'C': 'q609', 'c': 'q609'},
    'q609': {'K': 'q610', 'k': 'q610'},
    'q61': {'N': 'q62', 'n': 'q62'},
    'q610': {'D': 'q611', 'd': 'q611'},
    'q611': {'R': 'q612', 'r': 'q612'},
    'q612': {'O': 'q613', 'o': 'q613'},
    'q613': {'P': 'q614', 'p': 'q614'},
    'q614': {'P': 'q615', 'p': 'q615'},
    'q615': {'E': 'q616', 'e': 'q616'},
    'q616': {'R': 'q617', 'r': 'q617'},
    'q617': {'R': 'q618', 'r': 'q618'},
    'q618': {'U': 'q619', 'u': 'q619'},
    'q619': {'N': 'q620', 'n': 'q620'},
    'q62': {'P': 'q63', 'p': 'q63'},
    'q620': {'E': 'q621', 'e': 'q621'},
    'q621': {'D': 'q622', 'd': 'q622'},
    'q622': {'R': 'q623', 'r': 'q623'},
    'q623': {'O': 'q624', 'o': 'q624'},
    'q624': {'P': 'q625', 'p': 'q625'},
    'q625': {'P': 'q626', 'p': 'q626'},
    'q626': {'E': 'q627', 'e': 'q627'},
    'q627': {'R': 'q628', 'r': 'q628'},
    'q628': {'S': 'q629', 's': 'q629'},
    'q629': {'P': 'q630', 'p': 'q630'},
    'q63': {'O': 'q64', 'o': 'q64'},
    'q630': {'I': 'q631', 'i': 'q631'},
    'q631': {'D': 'q632', 'd': 'q632'},
    'q632': {'E': 'q633', 'e': 'q633'},
    'q633': {'R': 'q634', 'r': 'q634'},
    'q634': {'D': 'q635', 'd': 'q635'},
    'q635': {'R': 'q636', 'r': 'q636'},
    'q636': {'O': 'q637', 'o': 'q637'},
    'q637': {'P': 'q638', 'p': 'q638'},
    'q638': {'P': 'q639', 'p': 'q639'},
    'q639': {'E': 'q640', 'e': 'q640'},
    'q64': {'I': 'q65', 'i': 'q65'},
    'q640': {'R': 'q641', 'r': 'q641'},
    'q641': {'T': 'q642', 't': 'q642'},
    'q642': {'O': 'q643', 'o': 'q643'},
    'q643': {'R': 'q644', 'r': 'q644'},
    'q644': {'C': 'q645', 'c': 'q645'},
    'q645': {'H': 'q646', 'h': 'q646'},
    'q646': {'D': 'q647', 'd': 'q647'},
    'q647': {'R': 'q648', 'r': 'q648'},
    'q648': {'O': 'q649', 'o': 'q649'},
    'q649': {'P': 'q650', 'p': 'q650'},
    'q65': {'N': 'q66', 'n': 'q66'},
    'q650': {'P': 'q651', 'p': 'q651'},
    'q651': {'E': 'q652', 'e': 'q652'},
    'q652': {'R': 'q653', 'r': 'q653'},
    'q653': {'G': 'q654', 'g': 'q654'},
    'q654': {'H': 'q655', 'h': 'q655'},
    'q655': {'A': 'q656', 'a': 'q656'},
    'q656': {'S': 'q657', 's': 'q657'},
    'q657': {'T': 'q658', 't': 'q658'},
    'q658': {'D': 'q659', 'd': 'q659'},
    'q659': {'R': 'q660', 'r': 'q660'},
    'q66': {'T': 'q67', 't': 'q67'},
    'q660': {'O': 'q661', 'o': 'q661'},
    'q661': {'P': 'q662', 'p': 'q662'},
    'q662': {'P': 'q663', 'p': 'q663'},
    'q663': {'E': 'q664', 'e': 'q664'},
    'q664': {'R': 'q665', 'r': 'q665'},
    'q665': {'C': 'q666', 'c': 'q666'},
    'q666': {'H': 'q667', 'h': 'q667'},
    'q667': {'E': 'q668', 'e': 'q668'},
    'q668': {'S': 'q669', 's': 'q669'},
    'q669': {'T': 'q670', 't': 'q670'},
    'q67': {'O': 'q68', 'o': 'q68'},
    'q670': {'D': 'q671', 'd': 'q671'},
    'q671': {'R': 'q672', 'r': 'q672'},
    'q672': {'O': 'q673', 'o': 'q673'},
    'q673': {'P': 'q674', 'p': 'q674'},
    'q674': {'P': 'q675', 'p': 'q675'},
    'q675': {'E': 'q676', 'e': 'q676'},
    'q676': {'R': 'q677', 'r': 'q677'},
    'q677': {'B': 'q678', 'b': 'q678'},
    'q678': {'O': 'q679', 'o': 'q679'},
    'q679': {'O': 'q680', 'o': 'q680'},
    'q68': {'B': 'q69', 'b': 'q69'},
    'q680': {'K': 'q681', 'k': 'q681'},
    'q681': {'D': 'q682', 'd': 'q682'},
    'q682': {'R': 'q683', 'r': 'q683'},
    'q683': {'O': 'q684', 'o': 'q684'},
    'q684': {'P': 'q685', 'p': 'q685'},
    'q685': {'P': 'q686', 'p': 'q686'},
    'q686': {'E': 'q687', 'e': 'q687'},
    'q687': {'R': 'q688', 'r': 'q688'},
    'q688': {'S': 'q689', 's': 'q689'},
    'q689': {'H': 'q690', 'h': 'q690'},
    'q69': {'S': 'q70', 's': 'q70'},
    'q690': {'E': 'q691', 'e': 'q691'},
    'q691': {'L': 'q692', 'l': 'q692'},
    'q692': {'F': 'q693', 'f': 'q693'},
    'q693': {';': 'q694'},
    'q694': {'W': 'q695', 'w': 'q695'},
    'q695': {'O': 'q696', 'o': 'q696'},
    'q696': {'R': 'q697', 'r': 'q697'},
    'q697': {'L': 'q698', 'l': 'q698'},
    'q698': {'D': 'q699', 'd': 'q699'},
    'q699': {'S': 'q700', 's': 'q700'},
    'q7': {'M': 'q8', 'm': 'q8'},
    'q70': {'I': 'q71', 'i': 'q71'},
    'q700': {'A': 'q701', 'a': 'q701'},
    'q701': {'V': 'q702', 'v': 'q702'},
    'q702': {'E': 'q703', 'e': 'q703'},
    'q71': {'D': 'q72', 'd': 'q72'},
    'q72': {'I': 'q73', 'i': 'q73'},
    'q73': {'A': 'q74', 'a': 'q74'},
    'q74': {'N': 'q75', 'n': 'q75'},
    'q75': {'A': 'q76', 'a': 'q76'},
    'q76': {'N': 'q77', 'n': 'q77'},
    'q77': {'V': 'q78', 'v': 'q78'},
    'q78': {'I': 'q79', 'i': 'q79'},
    'q79': {'L': 'q80', 'l': 'q80'},
    'q8': {'E': 'q9', 'e': 'q9'},
    'q80': {'S': 'q81', 's': 'q81'},
    'q81': {'T': 'q82', 't': 'q82'},
    'q82': {'A': 'q83', 'a': 'q83'},
    'q83': {'C': 'q84', 'c': 'q84'},
    'q84': {'K': 'q85', 'k': 'q85'},
    'q85': {'R': 'q86', 'r': 'q86'},
    'q86': {'U': 'q87', 'u': 'q87'},
    'q87': {'N': 'q88', 'n': 'q88'},
    'q88': {'E': 'q89', 'e': 'q89'},
    'q89': {'S': 'q90', 's': 'q90'},
    'q9': {':': 'q10'},
    'q90': {'P': 'q91', 'p': 'q91'},
    'q91': {'I': 'q92', 'i': 'q92'},
    'q92': {'D': 'q93', 'd': 'q93'},
    'q93': {'E': 'q94', 'e': 'q94'},
    'q94': {'R': 'q95', 'r': 'q95'},
    'q95': {'T': 'q96', 't': 'q96'},
    'q96': {'O': 'q97', 'o': 'q97'},
    'q97': {'R': 'q98', 'r': 'q98'},
    'q98': {'C': 'q99', 'c': 'q99'},
    'q99': {'H': 'q100', 'h': 'q100'}
 }

Accepting States:{
    'q10': 'OPEN_WORLD',
    'q100': 'TYPE_TORCH',
    'q105': 'TYPE_CHEST',
    'q109': 'TYPE_BOOK',
    'q114': 'TYPE_GHAST',
    'q119': 'TYPE_SHELF',
    'q125': 'TYPE_ENTITY',
    'q133': 'TORCH_LITERALS',
    'q148': 'GHAST_LIRERALS',
    'q155': 'STACK_LITERALS',
    'q157': 'CHEST_LITERALS_LEFT',
    'q159': 'CHEST_LITERALS_RIGHT',
    'q160': 'CHEST_LITERAL_COMA',
    'q162': 'BOOK_LITERALS_LEFT',
    'q164': 'BOOK_LITERALS_RIGHT',
    'q17': 'BEDROCK',
    'q174': 'SPIDER_LITERALS',
    'q176': 'SHELF_LITERALS_LEFT',
    'q178': 'SHELF_LITERALS_RIGHT',
    'q179': 'ENTITY_LIT_LEFT',
    'q180': 'ENTITY_LIT_RIGHT',
    'q182': 'ASSIGN',
    'q191': 'ACCESS',
    'q193': 'FAMILY_SUM',
    'q195': 'FAMILY_SUB',
    'q197': 'FAMILY_MUL',
    'q199': 'FAMILY_DIV',
    'q201': 'FAMILY_REM',
    'q209': 'SOULSAND',
    'q214': 'MAGMA',
    'q229': 'IS_ENGRAVED',
    'q245': 'IS_INSCRIBED',
    'q251': 'ETCH_UP',
    'q259': 'ETCH_DOWN',
    'q262': 'AND',
    'q264': 'OR',
    'q267': 'NOT',
    'q270': 'XOR',
    'q274': 'BIND',
    'q275': 'LENGTH',
    'q279': 'FROM',
    'q281': 'OP',
    'q287': 'EXCEPT',
    'q29': 'RESOURCE_PACK',
    'q291': 'SEARCH',
    'q294': 'ADD',
    'q298': 'DROP',
    'q303': 'ITEMS',
    'q307': 'FEED',
    'q310': 'MAP',
    'q314': 'BIOM',
    'q318': 'KILL',
    'q324': 'UNLOCK',
    'q328': 'LOCK',
    'q333': 'CRAFT',
    'q339': 'GATHER',
    'q344': 'FORGE',
    'q350': 'EXPAND',
    'q352': 'FLOAT_ADD',
    'q354': 'FLOAT_SUB',
    'q356': 'FLOAT_MUL',
    'q358': 'FLOAT_REM',
    'q361': 'FLOAT_DIV',
    'q371': 'POLLO_CRUDO',
    'q38': 'INVENTORY',
    'q381': 'POLLO_ASADO',
    'q389': 'REPEATER',
    'q394': 'CRAFT',
    'q400': 'TARGET',
    'q403': 'HIT',
    'q407': 'MISS',
    'q414': 'JUKEBOX',
    'q418': 'DISC',
    'q425': 'SILENCE',
    'q432': 'SPAWNER',
    'q44': 'RECIPE',
    'q441': 'EXHAUSTED',
    'q445': 'WALK',
    'q447': 'TO',
    'q451': 'STEP',
    'q457': 'WITHER',
    'q464': 'CREEPER',
    'q474': 'ENDER_PEARL',
    'q482': 'RAGEQUIT',
    'q487': 'SPELL',
    'q493': 'RITUAL',
    'q494': 'PARAM_LEFT',
    'q495': 'PARAM_RIGHT',
    'q497': 'REF_PARAM',
    'q504': 'RESPAWN',
    'q509': 'CHUNK',
    'q511': 'TYPE_COHERTION',
    'q522': 'HOPPER_STACK',
    'q532': 'HOPPER_RUNE',
    'q544': 'HOPPER_SPIDER',
    'q555': 'HOPPER_TORCH',
    'q566': 'HOPPER_GHAST',
    'q57': 'CRAFTING_TABLE',
    'q577': 'HOPPER_CHEST',
    'q587': 'HOPPER_BOOK',
    'q598': 'HOPPER_SHELF',
    'q610': 'DROPPER_STACK',
    'q621': 'DROPPER_RUNE',
    'q634': 'DROPPER_SPIDER',
    'q646': 'DROPPER_TORCH',
    'q658': 'DROPPER_GHAST',
    'q67': 'SpawnPoint',
    'q670': 'DROPPER_CHEST',
    'q681': 'DROPPER_BOOK',
    'q693': 'DROPPER_SHELF',
    'q694': 'END_LINE',
    'q703': 'WORLD_SAVE',
    'q75': 'OBSIDIAN',
    'q80': 'ANVIL',
    'q85': 'TYPE_STACK',
    'q89': 'TYPE_RUNE',
    'q9': 'WORLD_NAME',
    'q95': 'TYPE_SPIDER'
 }

def build_dfa(token_types):
    transition_table = {}
    accepting_states = {}

    state_counter = 0

    for token_name, pattern in token_types:
        # Preprocess pattern: remove \b and escaped symbols
        clean = pattern.replace(r'\b', '')
        clean = clean.replace(r'\:', ':').replace(r'\;', ';').replace(r'\(', '(').replace(r'\)', ')')
        clean = clean.replace(r'\-', '-').replace(r'\+', '+').replace(r'\*', '*').replace(r'\/', '/')
        clean = clean.replace(r'\%', '%').replace(r'\:', ':').replace(r'\=', '=')
        clean = clean.replace(r'{:', '{:').replace(r':}', ':}').replace(r'{/', '{/').replace(r'/}', '/}')
        clean = clean.replace(r'\:\:', '::').replace(r'\:\+', ':+').replace(r'\:\-', ':-').replace(r'\:\*', ':*')
        clean = clean.replace(r'\:\%', ':%').replace(r'\:\/\/', '://')

        current_state = 'q' + str(state_counter)
        state = current_state

        for char in clean:
            next_state = 'q' + str(state_counter + 1)
            if state not in transition_table:
                transition_table[state] = {}
            # Insert case insensitive transitions
            transition_table[state][char.lower()] = next_state
            transition_table[state][char.upper()] = next_state
            state = next_state
            state_counter += 1

        # Last state is accepting
        accepting_states[state] = token_name

    return transition_table, accepting_states

# Build DFA
transition_table, accepting_states = build_dfa(TOKEN_TYPES)

# Print it nicely
import pprint
pp = pprint.PrettyPrinter(width=150)

print("Transition Table:")
pp.pprint(transition_table)

print("\nAccepting States:")
pp.pprint(accepting_states)