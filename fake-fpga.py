#!env python

import struct
import codecs
from hashlib import sha256
import serial

def start(payload, nonce):
    if payload == None:
        return -1
    if nonce == None:
        nonce = 0
    else:
        print(str(len(nonce)))
        print(str(nonce))
        nonce = struct.unpack("i", nonce)

    print(str(payload))
    print(str(nonce))
    
def aoeuaoeu():
    i = 2080000000
    ii = i
    #i = 2083236893
    found = False
    j = 0
    while found == False:
        # 2083236893
        nonce = struct.pack("i", i)
        hash = sha256(sha256(a + nonce).digest()).digest()[::-1]

        if hash < dificult:
            print("bingo! " + str(i - ii))
            found = True
        i = i + 1    

ser = serial.Serial('/dev/pts/7', 9600, rtscts=True,dsrdtr=True)

payload = None
nonce = None

run = True
while run == True:
    line = ser.readline()
    
    if len(line) == 0:
        continue
    
    if chr(line[0]) == "p":
        payload = line[2:]
    elif chr(line[0]) == "n":
        nonce = line[2:]
    elif chr(line[0]) == ">":
        start(payload, nonce)
        ser.write("Done: 123")
    elif chr(line[0]) == "!":
        pass
    else:
        print("*** Ops: " + str(chr(line[0])))
        print("*** " + str(line))
