
import socket


def xor(a, b):
    result = []
    for i in range(1, len(b)):
        if a[i] == b[i]:
            result.append('0')
        else:
            result.append('1')
    return ''.join(result)


def mod2div(divident, divisor):
    pick = len(divisor)
    tmp = divident[0: pick]
    while pick < len(divident):

        if tmp[0] == '1':

            tmp = xor(divisor, tmp) + divident[pick]

        else:

            tmp = xor('0'*pick, tmp) + divident[pick]

        pick += 1

    if tmp[0] == '1':
        tmp = xor(divisor, tmp)
    else:
        tmp = xor('0'*pick, tmp)

    checkword = tmp
    return checkword


def encodeData(data, key):

    l_key = len(key)

    appended_data = data + '0'*(l_key-1)
    remainder = mod2div(appended_data, key)

    return remainder


def decodeData(data, key):

    l_key = len(key)

    appended_data = data + '0'*(l_key-1)
    remainder = mod2div(appended_data, key)

    return remainder


def validate_remainder(remainder):
    if remainder == '000':
        print('Segun CRC-32 la cadena bitarray NO presenta error alguno\n')
    else:
        print('Segun CRC-32 la cadena bitarray SI presenta error alguno\n')
# Emisor


# data = input("Enter data you want to send->")
# print(data)
# key = "1001"
# ans = encodeData(data, key)
# print(ans)

# # Receptor
# res = decodeData(ans, key)
# print("Remainder after decoding is->"+res)
# validate_remainder(res)
