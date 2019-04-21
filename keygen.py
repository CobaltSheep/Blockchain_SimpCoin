import random
import math
import base64


#this performs euclids and extended euclids, which determines a value for d, using e and totientn
#a is e, and b is totient of n
#I received a lot of help from Chris Wu to write this
def euclids(a,b):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    totin = b

    while a > 0:
        temp1 = int(totin/a)
        temp2 = totin - (temp1 * a)
        totin = a
        a = temp2

        x = x2- temp1* x1
        y = d - temp1 * y1

        x2 = x1
        x1 = x
        d = y1
        y1 = y
        if a == 1:
            d = y1
            if d > 0:
                return d
            else:
                return d+b
            break

#determines a prime number from a certain bitlength and then returns a prime number in a small range under that bitlength
def getPrime(numBits):
    upperbound = 2**(numBits)
    lowerbound = 2**(numBits-2)

    num = random.randrange(lowerbound, upperbound, 1);

    if (not num & 1) and (num!=2):
        num = num+1

    def isPrime(num):
        if num == 2:
            return True
        if not num & 1:
            return False

        return pow(2, num-1, num) == 1

    while not isPrime(num):
        num = num + 2

        while num.bit_length() > numBits:
            num = num // 2

            if (not num & 1) and (num!=2):
                num = num+1
    return num

#converts the values for n and e into base64 and writes it to a file (public.key)
def encodePublic (n, e):
    n64 = base64.b64encode(n.to_bytes(math.ceil(n.bit_length()/8), 'little'));
    e64 = base64.b64encode(e.to_bytes(math.ceil(e.bit_length()/8), 'little'));
    n64decode = n64.decode();
    e64decode = e64.decode();
    print(n64decode + e64decode, file=open('public.key', 'w'), end='')

#converts the values for n and d into base64 and writes it to a file (private.key)
def encodePrivate (n, d):
    n64 = base64.b64encode(n.to_bytes(math.ceil(n.bit_length()/8), 'little'));
    d64 = base64.b64encode(d.to_bytes(math.ceil(d.bit_length()/8), 'little'));
    n64decode = n64.decode();
    d64decode = d64.decode();
    print(n64decode + d64decode, file=open('private.key', 'w'), end='')

if __name__ == '__main__':

    q = getPrime(2048);
    p = getPrime(2048);

    totientn = (p-1)*(q-1);
    totbit = totientn.bit_length()

    n = p*q;

    e = random.randrange(pow(2,300), totientn);
    while math.gcd(e,totientn) != 1:
        e = e + 1;

    d = euclids(e, totientn)


    M = 245
    C = pow( M, e, n)
    M = pow( C, d, n)


    encodePublic(n, e);
    encodePrivate(n, d);
