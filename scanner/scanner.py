import re # We are going to use this library to read regular expresions, for more info https://docs.python.org/3/library/re.htm

TOKEN_TYPES = [
    ("WORLD_NAME",          r'\bWorldName\b'),            #  Program title strcuture
    ("OPEN_WORLD",          r'\:'),

    # Sections  
    ("BEDROCK",             r'\bBedrock\b'),              #  Represents the constants (Values that will not change)
    ("RESOURCE_PACK",       r'\bResourcePack\b'),         #  Word used to define a new type
    ("INVENTORY",           r'\bInventory\b'),            #  If I need to declare a variable it will be in this section
    ("RECIPE",              r'\bRecipe\b'),               #  If I need to declare a fucntion it will be in this section
    ("CRAFTING_TABLE",      r'\bCraftingTable\b'),        #  Here we will have the "body" of the program
    ("SpawnPoint",          r'\bSpawnPoint\b'),           #  This is the "main" function of the program, where the program will start executing

    # Type declarations 
    ("OBSIDIAN",            r'\bObsidian\b'),             # To call constant we will use Obsidian with structure Obsidian <tipo> <id> <value>
    ("ANVIL",               r'\bAnvil\b'),                # To declare new variable types we will use Anvil with structure Anvil <id> -> <tipo>

    # ID types  
    ("TYPE_STACK",          r'\bStack\b'),                # Integer type we will use Stack with structure Stack <id> -> <value>
    ("TYPE_RUNE",           r'\bRune\b'),                 # Character type we will use Rune with structure Rune <id> -> <value>
    ("TYPE_SPIDER",         r'\bSpider\b'),               # String type we will use Spider with structure Spider <id> -> <value>
    ("TYPE_TORCH",          r'\bTorch\b'),                # Boolean type we will use Torch with structure Torch <id> -> <value>
    ("TYPE_CHEST",          r'\bChest\b'),                # Set type we will use Chest with structure 
    ("TYPE_BOOK",           r'\bBook\b'),                 # To take a text file we use Book with structure
    ("TYPE_GHAST",          r'\bGhast\b'),                # Float type will be used with Ghast with structure Ghast <id> -> <value>
    ("TYPE_SHELF",          r'\bShelf\b'),                # Array type will be used with Shelf with structure
    ("TYPE_ENTITY",         r'\bEntiy\b'),                # To declare registries we will use Entity with structure

    # Literals  
    ("TORCH_LITERALS",      r'(On\b|Off\b)'),           # Values for the Torch type
    ("STACK_LITERALS",      r'(-)?\d+'),                # Values for the Stack type, we will use an integer number
    ("GHAST_LIRERALS",      r'(-)?\d+(\.\d+)?'),        # Values for the Ghast type, we will use a float number
    ("CHEST_LITERALS_LEFT", r'{:'),                     # To open a set
    ("CHEST_LITERALS_RIGHT",r':}'),                     # To close a set
    ("BOOK_LITERALS_LEFT",  r'{/'),                     # To open a text file
    ("BOOK_LITERALS_RIGHT", r'/}'),                     # To close a text file
    ("SPIDER_LITERALS",     r'\"[^\"]*\"'),             # Values for the Spider type, we will use a string with double quotes
    ("SHELF_LITERALS_LEFT", r'\['),                     # To open an array
    ("SHELF_LITERALS_RIGHT",r'\]'),                     # To close an array
    ("ENTITY_LIT_LEFT",     r'{'),                      # To open a registry
    ("ENTITY_LIT_RIGHT",    r'}'),                      # To close a registry
    ("ASSIGN",               r'->'),                     # To asign a value to a variable we will use -> with structure <id> -> <value>

    # Access system: Refers to the way that we access the variables
    ("SHELF_ACCESS",        r'(\[\d\])+'),                      # For example [1, 2, 3, 4, 5]
    ("SPIDER_ACCESS",       r'[_a-zA-Z]\w*\[\d\]'),             # For example Value[2]
    ("ENTITY_ACCESS",       r'[_a-zA-Z]\w*\@[_a-zA-Z]\w*'),     # For exmple registro@Value

    # Family asignation
    ("FAMILY_ASIGNATION",   r'(\+|\-|\*|\/|\%)?='),     # The basic asingnation and 
    ("SOULSAND",            r'\bsoulsand\b'),
    ("MAGMA",               r'\bmagma\b'),

    # Basic operations: isEngraved, isInscribed, etchUp, etchDown, and, or, not, xor

    ("IS_ENGRAVED",          r'\bisEngraved(\?)?\b'),   #
    ("IS_INSCRIBED",         r'\bisInscribed(\?)?\b'),  #
    ("ETCH_UP",              r'\betchUp\b'),            #
    ("ETCH_DOWN",            r'\betchDown\b'),          #
    ("AND",                 r'\band\b'),                # 
    ("OR",                  r'\bor\b'),                 # 
    ("NOT",                 r'\bnot\b'),                # 
    ("XOR",                 r'\bxor\b'),                #
    
    # String operations: bind(concat), #(length), from  ##(cut), except  ##(extract), seek(search)
    ("BIND",                r'\bbind\b'),               #
    ("LENGTH",              r'\b#\b'),                  #
    ("OP",                  r'\b##\b'),                 # 
    ("EXTRACT",             r'\bexcept\b'),             # 
    ("SEARCH",              r'\bseek\b'),               #

    #Set operations: add(add), drop(delete), items(join), feed(intersect), map(belongs), biom(subset), kill(empty)
    ("ADD",                 r'\badd\b'),                #
    ("DROP",                r'\bdrop\b'),               #
    ("ITEMS",               r'\bitems\b'),              # 
    ("FEED",                r'\bfeed\b'),               # 
    ("MAP",                 r'\bmap\b'),                # 
    ("BIOM",                r'\bbiom\b'),               # 
    ("KILL",                r'\bkill\b'),               #

    # File operations: unlock(open), lock(close), craft(create), gather(read), forge(write), expand(join)
    ("UNLOCK",              r'\bunlock\b'),             #
    ("LOCK",                r'\block\b'),               # 
    ("CRAFT",               r'\bcraft\b'),              # 
    ("GATHER",              r'\bgather\b'),             # 
    ("FORGE",               r'\bforge\b'),              # 
    ("EXPAND",              r'\bexpand\b'),             #

    # FLoat operations :+, :-, :*, :%, ://
    ("FLOAT_OP",           r':\+|:-|:\*|:%|://'),       #
    
    # Instruction block: PolloCrudo, PolloAsado
    ("POLLO_CRUDO",         r'\bPolloCrudo\b'),         # 
    ("POLLO_ASADO",         r'\bPolloAsado\b'),         #

    # Instructions: repeater <cond> craft <instruction> (while), target <cond> craft hit <inst> miss <inst> (if-then-else)
    # jukebox <condition> craft , disc <case> : , silence (switch), spawner   <instrucciones>  exhausted   <cond> ;
    # walk VAR <exp> to <exp> step <exp> craft <instrucción> (For), wither <Referencia a Record> craft <instrucción> (With)
    # creeper (break), enderPearl(continue), ragequit(Halt)

    ("REPEATER",            r'\brepeater\b'),           #
    ("CRAFT",               r'\bcraft\b'),              #
    ("TARGET",              r'\btarget\b'),             #
    ("HIT",                 r'\bhit\b'),                # 
    ("MISS",                r'\bmiss\b'),               # 
    ("JUKEBOX",             r'\bjukebox\b'),            #
    ("DISC",                r'\bdisc\b'),               #
    ("SILENCE",             r'\bsilence\b'),            # 
    ("SPAWNER",             r'\bspawner\b'),            #
    ("TO",                  r'\bto\b'),                 #
    ("STEP",                r'\bstep\b'),               #
    ("EXHAUSTED",           r'\bexhausted\b'),          # 
    ("WALK",                r'\bwalk\b'),               # 
    ("WITHER",              r'\bwither\b'),             # 
    ("CREEPER",             r'\bcreeper\b'),            # 
    ("ENDER_PEARL",         r'\benderPearl\b'),         # 
    ("RAGEQUIT",            r'\bragequit\b'),           #

    # Headers: Spell(Function), Ritual(Procedure)
    ("SPELL",               r'\bSpell\b'),               # 
    ("RITUAL",              r'\bRitual\b'),              #

    # Formal parameters: ( <type> :: <name>, <name>;  <type> ref <name>;  … )
    ("PARAM_LEFT",          r'\('),                     # 
    ("PARAM_RIGHT",         r'\)'),                     #
    ("REF_PARAM",           r'\:\:'),                   #

    # Instructions
    ("RESPAWN",             r'\brespawn\b'),               # When we need to return as part of a function
    ("CHUNK",               r'\bchunk\b'),                 # Size of operation

    # Type cohertion
    ("TYPE_COHERTION",      r'>>'),                     # To convert a type to another type we will use >> with structure <id> >> <tipo>

    # Standart Input
    ("HOPPER_STACK",        r'\bhopperStack\b'),              # It requests an integer(stack) value from the user
    ("HOPPER_RUNE",         r'\bhopperRune\b'),               # It requests a character(rune) value from the user
    ("HOPPER_SPIDER",       r'\bhopperSpider\b'),             # It requests a string(spider) value from the user
    ("HOPPER_TORCH",        r'\bhopperTorch\b'),              # It requests a boolean(torch) value from the user
    ("HOPPER_GHAST",        r'\bhopperGhast\b'),              # It requests a float(ghast) value from the user
    ("HOPPER_CHEST",        r'\bhopperChest\b'),              # It requests a set(chest) value from the user
    ("HOPPER_BOOK",         r'\bhopperBook\b'),               # It requests a text(book) value from the user
    ("HOPPER_SHELF",        r'\bhopperShelf\b'),              # It requests an array(shelf) value from the user

    # Standart Output"DROPPER_STACK",r'\bdropperStack\b'),              # It prints an integer(stack) value to the user
    ("DROPPER_RUNE",        r'\bdropperRune\b'),               # It prints a character(rune) value to the user
    ("DROPPER_SPIDER",      r'\bdropperSpider\b'),             # It prints a string(spider) value to the user
    ("DROPPER_TORCH",       r'\bdropperTorch\b'),              # It prints a boolean(torch) value to the user
    ("DROPPER_GHAST",       r'\bdropperGhast\b'),              # It prints a float(ghast) value to the user
    ("DROPPER_CHEST",       r'\bdropperChest\b'),              # It prints a set(chest) value to the user
    ("DROPPER_BOOK",        r'\bdropperBook\b'),               # It prints a text(book) value to the user
    ("DROPPER_SHELF",       r'\bdropperShelf\b'),              # It prints an array(shelf) value to the user

    # End of line
    ("END_LINE",            r';'),                      # To end a line we will use ;

    # End of program
    ("WORLD_SAVE",         r'\bworldSave\b'),           # To end a program we will use End with structure worldSave

    #Comments
    ("LINE_COMMENT",        r'$$\w*'),                  # To add a comment we will use $$ with structure $$ <comment>
    ("BLOCK_COMMENT",       r'$\*\w\*$'),               # To add a comment we will use $* with structure $* <comment> $*

    # Identifiers
    ("ID",                  r'[_a-zA-Z]\w*'),           # 
    ("NUMBER",              r'\d+')
]

token_exprs = [(typ, re.compile(regex)) for typ, regex in TOKEN_TYPES]

def tokenize(code):
    pos = 0
    tokens = []

    while pos < len(code):
        match = None

        if code[pos].isspace():
            pos += 1
            continue

        for token_type, regex in token_exprs:
            match_obj = regex.match(code, pos)
            if match_obj:
                text = match_obj.group(0)
                match = (token_type, text)
                break
        
        if not match:
            raise SyntaxError(f"Illegal character at position {pos}: '{code[pos]}'")

        token_type, value = match
        if token_type not in ['LINE_COMMENT', 'BLOCK_COMMENT']:  # O ajusta según si quieres tokens de comentarios
            tokens.append((token_type, value))
        pos += len(value)

    return tokens

if __name__ == "__main__":
    test_code = '''WorldName Overworld:

        Bedrock
        Obsidian Stack MAX_HEALTH 100;
        Obsidian Torch LIGHT On;

        ResourcePack: BlockID: Stack;
        Anvil Speed -> Ghast;

        Inventory
        Stack life = 10
        Stack armor = 5;
        Torch light = On;

        Recipe
        Spell heal( Stack :: amount ) -> Stack;

        CraftingTable
        Spell heal( Stack :: amount ) -> Stack;
        PolloCrudo
            life += amount;
            respawn life;
        PolloAsado

        SpawnPoint
        PolloCrudo
            dropperStack(life);
            life += 2;
            light = Off;
            heal(5);
            creeper;
        PolloAsado

    worldSave

    '''

    tokens = tokenize(test_code)
    for t in tokens:
        print(t)
