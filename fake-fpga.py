#!/usr/bin/env python


from hashlib import sha256
import codecs
import getopt
import serial
import struct
import sys


def start(payload, nonce, dificult):
    if payload == None:
        return -1
    if nonce == None:
        nonce = 0
    else:
        nonce = struct.unpack("i", nonce)[0]

    print("Payload:  " + str(payload))
    print("Nonce:    " + str(nonce))
    print("Dificult: " + str(dificult))

    i = nonce
    while True:
        # 2083236893
        nonce = struct.pack("i", i)
        hash = sha256(sha256(payload + nonce).digest()).digest()[::-1]

        if hash < dificult:
            return i
        i = i + 1
        print(str(i))
    return None


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hvn:t:", ["help"])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

    verbose = False
    nonce = -1
    tty = None

    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-n", "--nonce"):
            nonce = int(a)
        elif o in ("-t", "--tty"):
            tty = str(a)
        else:
            assert False, "unhandled option"


    if nonce == -1:
        nonce = 2080000000

    if tty == None:
        tty = '/dev/pts/6'
    
    ser = serial.Serial(tty, 9600, rtscts=True, dsrdtr=True)

    payload = None
    dificult = None

    while True:
        line = ser.readline()
    
        if len(line) == 0:
            continue

        if chr(line[0]) == "p":
            payload = line[2:-1]
            #ser.write("payload loaded.")
        elif chr(line[0]) == "n":
            nonce = line[1:-1]
        elif chr(line[0]) == "d":
            dificult = line[1:-1]
            #ser.write("nonce loaded.")
        elif chr(line[0]) == ">":
            nonce = start(payload, nonce, dificult)
            if nonce != None:
                #o = codecs.decode(nonce, 'hex')
                ser.write(bytearray("done: ", "utf-8"))
                ser.write(bytearray(str(nonce), "utf-8"))
                ser.write(bytearray("\n", "utf-8"))
            else:
                ser.write(bytearray("failed"), "utf-8")
        elif chr(line[0]) == "!":
            pass
        else:
            print("*** Ops: " + str(chr(line[0])))
            print("*** " + str(line))


if __name__ == "__main__":
    main()

