# read a qr based on an image in path
# return the text

from crc import decodeData, encodeData, validate_remainder
import codecs
import pickle

from HammingCode import detectError
import socket

# Prueba de receptor de socket
def append_to_file(string, file_name):
    with open(file_name, 'a') as file:
        file.write(string)
        file.write('\n')

def fletcher16(data):
    sum1 = 0
    sum2 = 0
    for i in range(len(data)):
        sum1 = (sum1 + data[i]) % 255
        sum2 = (sum2 + sum1) % 255
    return (sum2 << 8) + sum1

def bitarray_to_string(data):
    return data.tobytes().decode('UTF-8')

def receptor_socket():
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
        # data = codecs.encode(pickle.dumps(data), "hex").decode()
        data = pickle.loads(data)
        print("Recibido: ", data)

        if data['tipo_verificador'] == 'CRC':
            ans = list(data['cadena'])
            ans = ''.join(str(e) for e in ans)
            # CRC-32 
            # Polynomial x32 + x26 + x23 + x22 + x16 + x12 + x11 + x10 + x8 + x7 + x5 + x4 + x2 + x + 1
            # Hex 0x 04 C1 1D B7
            key = '0100110000010001110110110111'
            de = decodeData(str(ans), key)
            print(de)
            validate_remainder(de)
            append_to_file(''.join([str(n) for n in data['cadena']]), 'CRC.txt')


        if data['tipo_verificador'] == 'fletcher16':
            if fletcher16(data['cadena']) == data['verificador']:
                print("Mensaje correcto segun fletcher16")
                append_to_file('correcto', 'fletcherAccuracy.txt')
            else:
                print("Mensaje incorrecto segun fletcher16")
                append_to_file('malo', 'fletcherAccuracy.txt')

            try:
                print(bitarray_to_string(data['cadena']))
            except:
                print('No se puede decodificar')

            append_to_file(''.join([str(n) for n in data['cadena']]), 'fletcher.txt')
            
            


        if data['tipo_verificador'] == 'hamming':
            datos_copia = list(data['cadena']).copy()
            correction = detectError(''.join(datos_copia), data['verificador'])
            if correction == 0:
                print("Mensaje correcto segun hamming")
            else:
                print("Mensaje incorrecto segun hamming")
                errorFound =len(datos_copia)-correction
                print("Se detecto un error en la posicion: ", errorFound)

                datos_copia[errorFound] = '1' if datos_copia[errorFound] == '0' else '0'
                print("Los datos corregidos son", ''.join(datos_copia))
                append_to_file(''.join(datos_copia), 'correction.txt')
                

        

        # print(data['tipo_verificador'])

        # if not data:
        #     break

        # temp = "0" * (len(key) - 1)
        # if ans == temp:
        #     c.sendall("THANK you Data ->"+data + " Received No error FOUND")
        # else:
        #     c.sendall("Error in data")

        c.close()
# Recibe el mensaje mediante un socket





receptor_socket()
