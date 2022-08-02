import pickle

from bitarray import bitarray
import random
import socket
from crc import decodeData, encodeData


# Para la verificación de Ida
def fletcher16(data):
    sum1 = 0
    sum2 = 0
    for i in range(len(data)):
        sum1 = (sum1 + data[i]) % 255
        sum2 = (sum2 + sum1) % 255
    return (sum2 << 8) + sum1


def isFailure(probabilidad):
    return random.random() < probabilidad


# Capa Aplicación
def enviarCadena(cadena):
    print("Introduzca su cadena: ", cadena)
    return cadena

# Capa de verificación


def enviarCadenaSegura(cadena, tipo_verificador = 'fletcher16'):
    a = bitarray()
    cadena = ascii(cadena)
    cadena = bytes(cadena, 'ASCII')
    # cadena=[cadena]
    # use bitarray to convert the string to a bitarray
    # cadena.
    # cadena = pickle.dumps(cadena)
    # cadena = bitarray(cadena)
    #print("Enviando: ", cadena)
    a.frombytes(cadena)
    if tipo_verificador == 'fletcher16':
        verificador= fletcher16(a)

    return a, verificador, tipo_verificador

# Capa de ruido


def agregarRuido(cadena):
    for n in range(len(cadena)):
        if isFailure(0.1):
            cadena[n] = not cadena[n]
    return cadena


def enviarObjeto(objeto):
    # Seriallización va acá
    print("Enviando: ", objeto)
    return objeto


def encode2(string):
    prueba = bitarray.bitarray()
    prueba.frombytes(string.encode('utf-8'))
    return prueba

# Prueba de funcion de socket


def emisor_socket(data):
    s = socket.socket()

    port = 12345

    s.connect(('127.0.0.1', port))
    s.sendall(data)
    s.close()
    return data



if __name__ == "__main__":
    mensaje_a_enviar = input("Introduzca su mensaje a enviar: \n")
    metodo_verificador = input("Introduzca el metodo de verificación \n")

    bit_data, verificador, tipo_verificador = enviarCadenaSegura(mensaje_a_enviar, metodo_verificador)
    bit_data = agregarRuido(bit_data)

    #envio de datos

    datos_serializados = pickle.dumps({'cadena': bit_data, 'verificador': verificador, 'tipo_verificador': tipo_verificador})
    emisor_socket(datos_serializados)
    # print(encode2('xddd'))
