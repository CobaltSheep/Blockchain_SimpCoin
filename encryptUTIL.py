import base64
import math

#reads the public.key and private.key files created after calling keygen.py. Decodes that information into int values for
#public and private keys
def read ():
    publicfile = open('public.key', 'r');
    fullpublic = publicfile.read();
    publiclength = len(fullpublic)//2;
    nvalue = fullpublic[:publiclength]
    n = str.encode(nvalue);
    n = base64.b64decode(n);
    n = int.from_bytes(n, 'little')
    evalue = fullpublic[publiclength:]
    e = str.encode(evalue);
    e = base64.b64decode(e);
    e = int.from_bytes(e, 'little')

    privatefile = open('private.key', 'r');
    fullprivate = privatefile.read();
    privatelength = len(fullprivate)//2;
    dvalue = fullprivate[privatelength:]
    d = str.encode(dvalue);
    d = base64.b64decode(d);
    d = int.from_bytes(d, 'little')

    return n,e,d;

# reads specifically from two keys directly to find n, e, and d
def readSpecial(publicread, privateread):
    n = None
    e = None
    d = None
    if(publicread is not None):
        publiclength = len(publicread)//2;
        nvalue = publicread[:publiclength]
        n = str.encode(nvalue);
        n = base64.b64decode(n);
        n = int.from_bytes(n, 'little')
        evalue = publicread[publiclength:]
        e = str.encode(evalue);
        e = base64.b64decode(e);
        e = int.from_bytes(e, 'little')

    if(privateread is not None):
        privatelength = len(privateread)//2;
        dvalue = privateread[privatelength:]
        d = str.encode(dvalue);
        d = base64.b64decode(d);
        d = int.from_bytes(d, 'little')

    return n,e,d;

#reads public key specifically and finds n and e values
def readPublic(publicread):
    publiclength = len(publicread)//2;
    nvalue = publicread[:publiclength]
    n = str.encode(nvalue);
    n = base64.b64decode(n);
    n = int.from_bytes(n, 'little')
    evalue = publicread[publiclength:]
    e = str.encode(evalue);
    e = base64.b64decode(e);
    e = int.from_bytes(e, 'little')

    return n,e;

#opens the inputfile and encrypts the message using the public key from read(),
#and then outputs in Base64
def encrypt (n, e, filename):
    inpfi = open(filename, 'r');
    inputfile = inpfi.read();
    inputfile = str.encode(inputfile);
    intmessage = int.from_bytes(inputfile, 'little');
    mencrypted = pow(intmessage, e, n);
    mencrypted = base64.b64encode(mencrypted.to_bytes(math.ceil(mencrypted.bit_length()/8), 'little'));
    mencrypted = mencrypted.decode();
    f = open(inputoutput, "w");
    f.write(mencrypted);
    f.close()
    return mencrypted;

#opens the inputfile and decrypts the message using the private key from read(),
#and then outputs in a string format
def decrypt (n, d, filename):
    inpfi = open(filename, 'r');
    inputfile = inpfi.read();
    inputfile = str.encode(inputfile);
    intencrypted = base64.b64decode(inputfile);
    encryptedmessage = int.from_bytes(intencrypted, 'little')
    mdecrypted = pow(encryptedmessage, d, n);
    mdecrypted = mdecrypted.to_bytes(math.ceil(mdecrypted.bit_length()/8), 'little');
    mdecrypted = mdecrypted.decode();
    f = open(inputoutput, "w");
    f.write(mdecrypted);
    f.close();
    return mdecrypted;

#opens the inputfile and encrypts the message using the private key from read(),
#and then outputs in Base64
def sign (n, d, filename):
    inpfi = open(filename, 'r');
    inputfile = inpfi.read();
    inputfile = str.encode(inputfile);
    intmessage = int.from_bytes(inputfile, 'little');
    msigned = pow(intmessage, d, n);
    msigned = base64.b64encode(msigned.to_bytes(math.ceil(n.bit_length()/8), 'little'));
    msigned = msigned.decode();
    f = open(inputoutput, "w");
    f.write(msigned);
    f.close()
    #print(msigned, file=f, end="");
    return msigned;

#signs the information but takes direct input instead of file
def signSpecial (n, d, in_put):
    in_put = str(in_put)
    input = str.encode(in_put);
    intmessage = int.from_bytes(input, 'little');
    msigned = pow(intmessage, d, n);
    msigned = base64.b64encode(msigned.to_bytes(math.ceil(n.bit_length()/8), 'little'));
    msigned = msigned.decode();
    #print(msigned, file=f, end="");
    return msigned;

#decrypts information but takes direct input instead of file
def decryptSpecial (n, d, in_put):
    input = str.encode(in_put);
    intencrypted = base64.b64decode(input);
    encryptedmessage = int.from_bytes(intencrypted, 'little')
    mdecrypted = pow(encryptedmessage, d, n);
    mdecrypted = mdecrypted.to_bytes(math.ceil(mdecrypted.bit_length()/8), 'little');
    mdecrypted = mdecrypted.decode();
    return mdecrypted;
