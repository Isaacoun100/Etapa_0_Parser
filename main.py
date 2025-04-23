
# Here we are going to design the command line interface that we will be
# using to interact with the user

welcome = ''' 
Instituto Tecnológico de Costa Rica
Ingeniería en Computación
Compiladores e intérpretes
Isaac Herrera Monge
Mauro Navarro Obando

Bienvenid@ al scanner de Notch Engine
Presiona:
    1. Para iniciarliza el scanner
    2. Para finalizar el scanning
    3. Para recibir el siguiente token DemeToken()
    4. Para aceptar el token TomeToke()
    '''

print(welcome)

while(True):
    response = input()

    match response:
        case "1":
            print("Iniciando el scanner...")
            # Aquí se inicializa el scanner
        case "2":
            print("Finalizando el scanning...")
            # Aquí se finaliza el scanning
        case "3":
            print("El token siguiente es:")
            # It reads the token and it identifies what familiy belongs to
            # then it shows to the user the family code, token, translated
            # value, line and column, and error line if necessary
        case "4":
            print("Aceptamos el token")
            # Here we decide if the token is going to be accepted or not
        case _:
            print("Opción no válida. Por favor, ingrese una opción válida.")
            # Aquí se maneja la opción no válida