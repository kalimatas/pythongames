#!/usr/bin/env python

MAXKEYLEN = 26

def getMode():
    while True:
        print("Encrypt or decrypt or btute?")
        mode = input().lower()
        if mode in 'encrypt e decrypt d brute b'.split():
            return mode
        else:
            print('Enter "encrypt|e|decrypt|d|brute|b"')

def getMessage():
    print('Enter your message: ')
    return input()

def getKey():
    key = 0
    while True:
        print('Enter the key (1-%s)' % (MAXKEYLEN))
        key = int(input())
        if (key >= 1 and key <= MAXKEYLEN):
            return key

def getTranslatedMessage(mode, message, key):
    if mode[0] == 'd':
        key = -key
    translated = ''

    for symbol in message:
        if symbol.isalpha():
            num = ord(symbol)
            num += key

            if symbol.isupper():
                if num > ord('Z'):
                    num -= 26
                elif num < ord('A'):
                    num += 26
            elif symbol.islower():
                if num > ord('z'):
                    num -= 26
                elif num < ord('a'):
                    num += 26

            translated += chr(num)
        else:
            translated += symbol

    return translated

if __name__ == "__main__":
    mode = getMode()
    message = getMessage()
    if mode[0] != 'b':
        key = getKey()
    
    print('You text is: ')
    if mode[0] != 'b':
        print(getTranslatedMessage(mode, message, key))
    else:
        for key in range(1, MAXKEYLEN + 1):
            print(key, getTranslatedMessage('d', message, key))
    
    
