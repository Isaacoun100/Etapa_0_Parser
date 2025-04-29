WorldName  printNumbers :

Bedrock  $$ Aqui tenemos las constantes

ResourcePack $$ En esta seccion se crea tipos
    Anvil example -> Stack;
    Anvil value -> Spider;

Inventory $$ Declaracion de variables
    Stack printing = 20;

Recipe

    repeater printing > 0 craft:
    PolloCrudo
        dropperStack(printing)
        printing -= printing
    PolloAsado

worldSave 