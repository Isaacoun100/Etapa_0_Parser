import re # We are going to use this library to read regular expresions, for more info https://docs.python.org/3/library/re.html

# ("NUMBER",    r'\d+'),
TOKEN_TYPES = [
    ("WORLD_NAME",          r'WorldName\b'),        #  Program title strcuture

    # Sections
    ("BEDROCK",             r'Bedrock\b'),          #  Represents the constants (Values that will not change)
    ("RESOURCE_PACK",       r'ResourcePack\b'),     #  Word used to define a new type
    ("INVENTORY",           r'Inventory\b'),        #  If I need to declare a variable it will be in this section
    ("RECIPE",              r'Recipe\b'),           #  If I need to declare a fucntion it will be in this section
    ("CRAFTING_TABLE",      r'CraftingTable\b'),    #  Here we will have the "body" of the program
    ("SpawnPoint",          r'SpawnPoint\b'),       #  This is the "main" function of the program, where the program will start executing

    # Type declarations
    ("OBSIDIAN",            r'Obsidian\b'),         # To call constant we will use Obsidian with structure Obsidian <tipo> <id> <value>
    ("ANVIL",               r'Anvil\b'),            # To declare new variable types we will use Anvil with structure Anvil <id> -> <tipo>
    
    # ID types
    ("TYPE_STACK",          r'Stack\b'),            # Integer type we will use Stack with structure Stack <id> -> <value>
    ("TYPE_RUNE",           r'Rune\b'),             # Character type we will use Rune with structure Rune <id> -> <value>
    ("TYPE_SPIDER",         r'Spider\b'),           # String type we will use Spider with structure Spider <id> -> <value>
    ("TYPE_TORCH",          r'Torch\b'),            # Boolean type we will use Torch with structure Torch <id> -> <value>
    ("TYPE_CHEST",          r'Chest\b'),            # Set type we will use Chest with structure 
    ("TYPE_BOOK",           r'Book\b'),             # To take a text file we use Book with structure
    ("TYPE_GHAST",          r'Ghast\b'),            # Float type will be used with Ghast with structure Ghast <id> -> <value>
    ("TYPE_SHELF",          r'Shelf\b'),            # Array type will be used with Shelf with structure
    ("TYPE_ENTITY",         r'Entiy\b'),            # To declare registries we will use Entity with structure

    # Literals
    ("TORCH_LITERALS",      r'(On\b|Off\b)'),       # To declare a literal we will use TorchLit with structure TorchLit <id> -> <value>
    ("CHEST_LITERALS_LEFT", r'{:'),                 # To open a set
    ("CHEST_LITERALS_RIGHT",r':}'),                 # To close a set
    ("BOOK_LITERALS_LEFT",  r'{/'),                 # To open a text file
    ("BOOK_LITERALS_RIGHT", r'/}'),                 # To close a text file
    ("GHAST_LIRERALS",       r'\d+(\.\d+)?'),       # To declare a float we will use GhastLit with structure GhastLit <id> -> <value>

    ("ID",                  r'[a-zA-Z_][a-zA-Z_0-9]*'),
    ("NUMBER",              r'\d+'),

]
