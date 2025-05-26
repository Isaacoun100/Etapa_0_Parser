WorldName  sumador :

Bedrock  $$ Aqui tenemos las constantes

ResourcePack $$ En esta seccion se crea tipos
    Anvil example -> Stack;
    Anvil value -> Spider;

Inventory $$ Declaracion de variables
    Stack firstValue = 10;
    Stack secondValue = 20;
    Ghast fvalue = 12.300;
    Stack result = 0;
    Stack counter = 0;
    Rune hello = "Hello!";

Recipe

    WALK counter SET 0 TO 10 STEP 1 CRAFT
        POLLOCRUDO
            result = firstValue * secondValue
            firstValue = firstValue ++;
            secondValue = secondValue --;
        POLLOASADO

    fvalue = fvalue :+300.12;
    firstValue = 300.12 :+ _fvalue;

    result += 1;
    result += fvalue;
    result -= 1;
    result -= fvalue;
    result *= 1;
    result *= fvalue;
    result /= 1;
    result /= fvalue;
    result %= 1;
    result %= fvalue;

    result = result + 5
    result = result - 5
    result = result * 5
    result = result // 5
    result = result % fvalue
    result = result + fvalue
    result = result - fvalue
    result = result * fvalue
    result = result // fvalue
    result = result % fvalue
    
    result = result :+ 5
    result = result :- 5
    result = result :* 5
    result = result :// 5
    result = result :% fvalue
    result = result :+ fvalue
    result = result :- fvalue
    result = result :* fvalue
    result = result :// fvalue
    result = result :% fvalue

worldSave