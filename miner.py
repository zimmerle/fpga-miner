#!/usr/bin/env python


from hashlib import sha256
import codecs
import getopt
import serial
import struct
import sys



def resolveLocal(payload, dificult, ts, nonce, device):
    payload = payload[0] + ts + payload[1]
    payload = codecs.decode(payload.upper(), 'hex')

    i = nonce
    ii = i
    j = 0

    print("Payload:  " + str(payload))
    print("Nonce:    " + str(nonce))
    print("Dificult: " + str(dificult))

    while True:
        nonce = struct.pack("i", i)
        hash = sha256(sha256(payload + nonce).digest()).digest()[::-1]
        if hash < dificult:
            return (i, ts)
        i = i + 1


def sendToFpga(a, dificult, ts, nonce, device):
    a = a[0] + ts + a[1]
    a = codecs.decode(a.upper(), 'hex')

    nonce = struct.pack("i", nonce)
    ser = serial.Serial(device, 9600, rtscts=True, dsrdtr=True)
    ser.write(bytes([0x70]) + bytes([0x20]) + a + bytes([0xa]))
    ser.write(bytes([0x6e]) + nonce + bytes([0xa]))
    ser.write(bytes([0x64]) + dificult + bytes([0xa]))
    ser.write(bytes([0x3e]) + bytes([0xa]))
    while True:
        line = ser.readline()

        if len(line) == 0:
            continue

        if line[0] == 100:
            #print(">>>> " + str(len(line[6:-1])))
            #print(">>>> " + str(line[6:-1]))
            return (codecs.decode(line[6:-1]), ts)

        if line[0] == 's':
            print("Status: " + line[2:])



def usage():
    print(sys.argv[0] + "")


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hlvn:t:", ["help", "local"])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

    verbose = False
    local = False
    nonce = -1
    tty = None
    ret = -1

    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-l", "--local"):
            local = True
        elif o in ("-n", "--nonce"):
            nonce = int(a)
        elif o in ("-t", "--tty"):
            tty = str(a)
        else:
            assert False, "unhandled option"


    if nonce == -1:
        nonce = 2083236883

    if tty == None:
        tty = '/dev/pts/6'

    version = "01000000"
    last_block = "0000000000000000000000000000000000000000000000000000000000000000"
    merkle_root = "4A5E1E4BAAB89F3A32518A88C31BC87F618F76673E2CC77AB2127B7AFDEDA33B"
    merkle_root = codecs.decode(merkle_root, 'hex')[::-1].hex()
    time_stamp = "29AB5F49" # January 03, 2009, 15:15:05 -0300
    bits = "FFFF001D"
    dificult = codecs.decode(format(0x00ffff * 2**(8*(0x1d - 3)), '02x').zfill(64), 'hex')

    toHash = [version + last_block + merkle_root, bits]
    


    if local:
        ret = resolveLocal(toHash, dificult, time_stamp, nonce, tty)
    else:
        ret = sendToFpga(toHash, dificult, time_stamp, nonce, tty)


    if ret == None:
        print("Failed to find the hash")
    else:
        (nonce, ts) = ret
        print("nonce: " + str(nonce))
        print("ts   : " + str(ts))


if __name__ == "__main__":
    main()

