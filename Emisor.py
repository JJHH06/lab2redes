import pickle
import time
from bitarray import bitarray
import random
import socket
from crc import decodeData, encodeData
from HammingCode import *

def append_to_file(string, file_name):
    with open(file_name, 'a') as file:
        file.write(string)
        file.write('\n')

#generate a random string of length n
def random_string(n):
    return ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for i in range(n))

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
        # CRC-32
        # Polynomial x32 + x26 + x23 + x22 + x16 + x12 + x11 + x10 + x8 + x7 + x5 + x4 + x2 + x + 1
        # Hex 0x 04 C1 1D B7
        key = '0100110000010001110110110111'
        lisData = ''.join(str(e) for e in list(a))
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


def agregarRuido(cadena, tasa_fallo=0.01, tipo='fletcher16'):
    new_list = []
    if tipo == 'hamming':
        for n in range(len(cadena)):
            if isFailure(tasa_fallo):
                if cadena[n] == '0':
                    new_list.append('1')
                else:
                    
                    new_list.append('0')
            else:
                new_list.append(cadena[n])
        return ''.join(new_list)
    else:
        for n in range(len(cadena)):
            if isFailure(tasa_fallo):
                cadena[n] = not cadena[n]
    new_list_str = ''.join(new_list)
    return cadena





def encode2(string):
    prueba = bitarray.bitarray()
    prueba.frombytes(string.encode('utf-8'))
    return prueba

# Prueba de funcion de socket

#Capa de envio
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

    # envio de datoshammin
    datos_serializados = pickle.dumps(
        {'cadena': bit_data, 'verificador': verificador, 'tipo_verificador': tipo_verificador})

    # para las graficas de Hamming
    # for i in range(10):
        # mensaje_a_enviar = random_string(10)
        # metodo_verificador = 'hamming'
        # bit_data, verificador, tipo_verificador = enviarCadenaSegura(
        # mensaje_a_enviar, metodo_verificador)
        # bit_data = agregarRuido(bit_data, 0.05, tipo_verificador)
        # datos_serializados = pickle.dumps(
        # {'cadena': bit_data, 'verificador': verificador, 'tipo_verificador': tipo_verificador})
        # append_to_file(bit_data, "original.txt")
        # emisor_socket(datos_serializados)

    # for i in range(100):
    #     mensaje_a_enviar = random_string(10)
    #     metodo_verificador = 'fletcher16'
    #     bit_data, verificador, tipo_verificador = enviarCadenaSegura(
    #     mensaje_a_enviar, metodo_verificador)
    #     bit_data = agregarRuido(bit_data, 0.05, tipo_verificador)
    #     datos_serializados = pickle.dumps(
    #     {'cadena': bit_data, 'verificador': verificador, 'tipo_verificador': tipo_verificador})
    #     append_to_file(''.join([str(n) for n in bit_data]), "originalfletcher.txt")
    #     emisor_socket(datos_serializados)
    #     time.sleep(0.2)
    

    # for i in range(100):
    #     mensaje_a_enviar = random_string(10)
    #     metodo_verificador = 'CRC'
    #     bit_data, verificador, tipo_verificador = enviarCadenaSegura(
    #     mensaje_a_enviar, metodo_verificador)
    #     bit_data = agregarRuido(bit_data, 0.05, tipo_verificador)
    #     datos_serializados = pickle.dumps(
    #     {'cadena': bit_data, 'verificador': verificador, 'tipo_verificador': tipo_verificador})
    #     append_to_file(''.join([str(n) for n in bit_data]), "originalCRC.txt")
    #     emisor_socket(datos_serializados)
    #     time.sleep(0.2)
