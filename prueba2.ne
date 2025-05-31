WorldName  printNumbers :

Bedrock  $$ Aqui tenemos las constantes

ResourcePack $$ En esta seccion se crea tipos
    Anvil example -> Stack;
    Anvil value -> Spider;

Inventory $$ Declaracion de variables
    Stack printing = 20;

Recipe
    spell func1 (num1) -> Stack
    spell func2 (num1) -> Rune
    ritual rut1 (str0);

CraftingTable
    RITUAL rut1 (str0)
    PolloCrudo
        creeper

    PolloAsado;

SpawnPoint
    Inventory $$ Declaracion de variables
    Stack counter = 20;
    PolloCrudo
       $*counter magma; No funciona por doble prediccion*$
       counter = counter - 3;
    PolloAsado;

worldSave 