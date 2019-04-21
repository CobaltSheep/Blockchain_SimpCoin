import socket
import requests
import keygen
import encryptUTIL
import threading
import json
import time
import random

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
server.bind(("0.0.0.0", 5001))

class Peer():
    '''
    constructor for peer class, assigns public key, address, 
    and Nonce from parameters
    '''
    def __init__(self, Nonce, publickey, address):
        self.address = address
        self.nonce = Nonce
        self.public_key = publickey
    
    '''
    takes all attributes and makes a dictionary, which then
    turns into a JSON and is returned
    '''
    def toJSON(self):
        peerjson = {}

        peerjson['address'] = self.address
        peerjson['nonce'] = self.nonce
        peerjson['pkey'] = self.public_key

        peerjson = json.dumps(peerjson)

        return peerjson

    '''
    returns string representation of PEER class by calling
    toJSON
    '''
    def __repr__(self):
        return toJSON()



client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# Set a timeout so the socket does not block
# indefinitely when trying to receive data.
client.settimeout(0.2)
message = {"coin":"simplecoin"}

publicBkey = open('publicB.key', 'r')
BPU = publicBkey.read()

privateBkey = open('privateB.key', 'r')
BPR = privateBkey.read()

b_n, b_e, b_d = encryptUTIL.readSpecial(BPU, BPR)
Nonce = random.randint(100000,1000000)
nonce_signed = encryptUTIL.signSpecial(b_n, b_d, Nonce)


information = {}
information['Nonce'] = nonce_signed
information['Public Key'] = BPU

infojson = json.dumps(information)

class UdpServer():

    '''
    constructor for UDP server which takes a peerlist and a lock and 
    creates a peerlist attribute as well as a lock attribute
    '''
    def __init__(self, peerlist, lock):
        self.peer_list = peerlist
        self.newlock = lock
    
    '''
    sends repeated broadcasts to potential peers at 5001
    port, does this every second
    '''
    def sendMessages(self, event):
        while not event.is_set():
            new = json.dumps(message)
            client.sendto(new.encode(), ('<broadcast>', 5001))
            time.sleep(1)
    
    '''
    receives messages sent by client, sends a post request to the 
    ledger with its public key and encrypted Nonce.
    Once ledger responds, adds ledger as peer as well as the ledger's
    peerlist to its own
    '''
    def receiveMessages(self, event):
        while not event.is_set():
            data, addr = server.recvfrom(1024)
            r = requests.post("http://"+ str(addr[0]) + ":8001/peers", infojson)
            response_json = r.json()
            nonce_encrypted = response_json['nonce'] 
            

            a = response_json['p_key']
            
            j_n, j_e, j_d = encryptUTIL.readSpecial(a, None)
            
            nonce_decrypted = encryptUTIL.decryptSpecial(j_n, j_e, nonce_encrypted)
            realnonce = str(Nonce)
            
            if(nonce_decrypted == realnonce):
                new_peer = Peer(realnonce, a, str(addr[0]))
                self.newlock.acquire()
                otherpeers = response_json['peerlist']
                somepeers = []
                for a in otherpeers:
                    p = json.loads(a)
                    peer = Peer(p['nonce'], p['pkey'], p['address'])
                    somepeers.append(peer)
            
                somepeers.append(new_peer)

                for peer in somepeers:
                    inside = False
                    for n in self.peer_list:
                        if(n.address == peer.address):
                            inside = True
                
                    if(inside == False):
                        self.peerlist.append(peer)       
                self.newlock.release() 
             

    ''' 
    runs the functions inside UDP in two separate threads so that
    the client and server can communicate
    This function is run by app.py
    '''
    def run(self, event):
        try:
            Thread1 = threading.Thread(target=self.sendMessages, args=(event,))
            Thread2 = threading.Thread(target=self.receiveMessages, args=(event,))
            Thread1.start()
            Thread2.start()
        except:
            print("thread did not work!")












