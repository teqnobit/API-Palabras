import random

palabrasConocidas = {"clave": "valor"}
palabrasPracticar = {"Would": "lo haria", "Witness": "testigo", "Whistle": "silvido"}
palabrasAprendidas = {"clave": "valor"}

def mostrarPalabras():
    # Extraemos las llaves
    listallaves = list(palabrasPracticar)
    
    # Randomizamos las opciones
    primerNum = random.randrange(len(listallaves))
    segundoNum = random.randrange(len(listallaves))
    tercerNum = random.randrange(len(listallaves))
    
    # Verificamos que no se repitan
    while segundoNum == primerNum:
        segundoNum = random.randrange(len(listallaves))
    while tercerNum == primerNum or tercerNum == segundoNum:
        tercerNum = random.randrange(len(listallaves))

    # Mostramos
    print(" -"+ listallaves[primerNum] +": "+ palabrasPracticar[listallaves[primerNum]])
    print(" -"+ listallaves[segundoNum] +": "+ palabrasPracticar[listallaves[segundoNum]])
    print(" -"+ listallaves[tercerNum] +": "+ palabrasPracticar[listallaves[tercerNum]])


def ingresarPalabras():
    nuevaPalabra = input("Introduce una nueva palabra: ").capitalize()

    # Verificamos que no se repitan
    listallaves = list(palabrasPracticar)
    if nuevaPalabra in listallaves:
        return print("Palabra ya en el diccionario")
    
    nuevaTraduccion = input("Introduce su traduccion: ").capitalize()

    # Ingresamos la palabra al diccionario
    palabrasPracticar[nuevaPalabra] = nuevaTraduccion
    print("Palabra registrada!")

if __name__ == "__main__":
    while True:
        print("** Que deseas hacer? **\n1) Practicar tres palabras\n2) Ingresar una palabra nueva")
        opcion = input("Introduce una opcion: ")
        if opcion == "1" or opcion == "2":
            if opcion == "1":
                mostrarPalabras()
            else:
                ingresarPalabras()
        else: 
            print("Opcion no valida")

