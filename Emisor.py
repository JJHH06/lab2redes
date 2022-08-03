import pickle

from bitarray import bitarray
import random
import socket
from crc import decodeData, encodeData
from HammingCode import *


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


def enviarCadenaSegura(cadena, tipo_verificador='fletcher16'):
    a = bitarray()
    cadena = ascii(cadena)
    cadena = bytes(cadena, 'ASCII')
    a.frombytes(cadena)
    print(tipo_verificador)

    if 'CRC' in tipo_verificador:
        b = bitarray()
        key = '1001'
        lisData = ''.join(str(e) for e in list(cadena))
        ans = encodeData(lisData, key)
        b.extend(ans)
        a = a.copy()+b
        verificador = ans
    if 'fletcher16' in tipo_verificador:
        verificador = fletcher16(a)
    if 'hamming' in tipo_verificador:
        a = ''.join([str(n) for n in a])
        tipo_verificador = 'hamming'
        m = len(a)
        r = calcRedundantBits(m)
        arr = posRedundantBits(a, r)
        arr = calcParityBits(arr, r)
        a = arr
        verificador = r

    return a, verificador, tipo_verificador

# Capa de ruido


def agregarRuido(cadena, tasa_fallo = 0.01 , tipo = 'fletcher16'):

    if tipo == 'hamming':
        for n in range(len(cadena)):
            if isFailure(tasa_fallo):
                if cadena[n] == '0':
                    cadena[n] = '1'
                else:
                    cadena[n] = '0'
    else:
        for n in range(len(cadena)):
            if isFailure(tasa_fallo):
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

    bit_data, verificador, tipo_verificador = enviarCadenaSegura(
        mensaje_a_enviar, metodo_verificador)
    bit_data = agregarRuido(bit_data, 0.5, tipo_verificador)

    # envio de datos

    datos_serializados = pickle.dumps(
        {'cadena': bit_data, 'verificador': verificador, 'tipo_verificador': tipo_verificador})
    emisor_socket(datos_serializados)
    # print(encode2('xddd'))
