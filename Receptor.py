# read a qr based on an image in path
# return the text

from crc import decodeData, encodeData

import socket

# Prueba de receptor de socket


def receptor_socket(data):
    s = socket.socket()

    print("Socket successfully created")

    port = 12345

    s.bind(('', port))
    print("socket binded to %s" % (port))
    s.listen(5)
    print("socket is listening")

    while True:

        c, addr = s.accept()
        print('Got connection from', addr)

        data = c.recv(1024)

        print(data)

        # if not data:
        #     break

        # temp = "0" * (len(key) - 1)
        # if ans == temp:
        #     c.sendall("THANK you Data ->"+data + " Received No error FOUND")
        # else:
        #     c.sendall("Error in data")

        c.close()
# Recibe el mensaje mediante un socket


def recibirObjeto(objeto):
    print("Enviando: ", objeto)
    return objeto


# Capa de verificacion
# J Convulcionales
# Marco CRC-32
# Christian Fletcher checksum
# Recibe el mensaje de bitarray y lo pasa por los algoritmos de correcion de errores.
def recibir_Cadena_segura(objeto):
    print("Enviando: ", objeto)
    return objeto


def recibir_cadena(objeto):
    print("Enviando: ", objeto)
    return objeto
