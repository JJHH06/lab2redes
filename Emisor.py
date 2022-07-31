import pickle

from bitarray import bitarray
import random

def isFailure(probabilidad):
   return random.random() < probabilidad



# Capa Aplicación
def enviarCadena(cadena):
    print("Introduzca su cadena: ", cadena)
    return cadena 

# Capa de verificación

def enviarCadenaSegura(cadena):
    a = bitarray()
    cadena=ascii(cadena)
    cadena=bytes(cadena,'ASCII')
    # cadena=[cadena]
    a.frombytes(cadena)
    # use bitarray to convert the string to a bitarray
    
    
    # cadena.
    # cadena = pickle.dumps(cadena)
    # cadena = bitarray(cadena)
    #print("Enviando: ", cadena)
    return a

# Capa de ruido
def agregarRuido(cadena):
    for n in range(len(cadena)):
        if isFailure(0.1):
            cadena[n] = not cadena[n]
    return cadena
    

def enviarObjeto(objeto):
    #Seriallización va acá
    print("Enviando: ", objeto)
    return objeto


def encode2(string):
    prueba = bitarray.bitarray()
    prueba.frombytes(string.encode('utf-8'))
    return prueba

#        ____()()
#       /      @@
# `~~~~~\_;m__m._>o

#run main()
if __name__ == "__main__":
    print(enviarCadenaSegura("xddd"))
    print(agregarRuido(enviarCadenaSegura("xddd")))
    #print(encode2('xddd'))