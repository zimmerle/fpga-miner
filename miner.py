#!env python

import struct
import codecs
from hashlib import sha256
import serial

def check(a):
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

def sendToFpga(a):
    nonce = struct.pack("i", 2080000000)
    run = True
    ser = serial.Serial('/dev/pts/6', 9600, rtscts=True,dsrdtr=True)
    #ser = serial.Serial('/dev/ttyS1', 115200, timeout=1)
    ser.write(bytes([0x70]) + bytes([0x20]) + a + bytes([0xa]))
    ser.write(bytes([0x6e]) + nonce + bytes([0xa]))
    ser.write(bytes([0x3e]) + bytes([0xa]))
    while run:
        line = ser.readline()
        if len(line) == 0:
            continue
        if line[0] == "d":
            print("Done: " + line[:1])
            run = False
        if line[0] == "s":
            print("Status: " + line[:1])


version = "01000000"
last_block = "0000000000000000000000000000000000000000000000000000000000000000"
merkle_root = "4A5E1E4BAAB89F3A32518A88C31BC87F618F76673E2CC77AB2127B7AFDEDA33B"
merkle_root = codecs.decode(merkle_root, 'hex')[::-1].hex()
time_stamp = "29AB5F49" # January 03, 2009, 15:15:05 -0300  
bits = "FFFF001D"
dificult = codecs.decode(format(0x00ffff * 2**(8*(0x1d - 3)), '02x').zfill(64), 'hex')

toHash = version + last_block + merkle_root + time_stamp \
    + bits
toHash = toHash.upper()
toHash = codecs.decode(toHash, 'hex')

if 1 == 0:
    check(toHash)
else:
    sendToFpga(toHash)
    


print("Done")
