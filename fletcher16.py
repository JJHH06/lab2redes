import bitarray
import random


def encode(string):
    prueba = bitarray.bitarray()
    prueba.frombytes(string.encode('ascii'))
    return prueba


def bitarray_to_string(data):
    return data.tobytes().decode('ascii')


def fletcher16(data):
    sum1 = 0
    sum2 = 0
    for i in range(len(data)):
        sum1 = (sum1 + data[i]) % 255
        sum2 = (sum2 + sum1) % 255
    return (sum2 << 8) + sum1


def apply_noise(data, p):
    lista = data
    for i in range(len(lista)):
        if random.random() < p:
            if lista[i] == 0:
                lista[i] = 1
            else:
                lista[i] = 0
    return lista


prueba = encode('Hola Mundo')
emisor = fletcher16(prueba)
prueba_ruido = apply_noise(prueba, 0.01)
receptor = fletcher16(prueba_ruido)

print(prueba)
print(emisor)
print(receptor)

if emisor == receptor:
    print('Los datos son correctos')
else:
    print('Los datos son incorrectos')

try:
    print(bitarray_to_string(prueba_ruido))
except:
    print('No se puede decodificar')
