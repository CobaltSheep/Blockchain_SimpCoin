from flask import Flask, render_template, request

from flask_sqlalchemy import SQLAlchemy

import encryptUTIL
import keygen
import mainfile
from mainfile import Transaction
from mainfile import BlockChain
import threading
import sys
import signal
import signal
import server
import json
import sqlite3



app = Flask(__name__)


def signal_handler(sig, frame):
    event.set()
    sys.exit(0)

#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databases.sqlite3'
db = SQLAlchemy(app)

class blockchains(db.Model):
    id = db.Column('student_id', db.Integer, primary_key = True)
    system_public = db.Column(db.String())
    system_private = db.Column(db.String()) 

    def __init__(self, system_public, system_private):
        self.system_public = system_public
        self.system_private = system_private

class blocks(db.Model):
    id = db.Column('student_id', db.Integer, primary_key = True)
    timestamp = db.Column(db.String())
    nonce = db.Column(db.Int())
    


    def __init__(self, system_public, system_private):
        self.system_public = system_public
        self.system_private = system_private

class transactions(db.Model):
    id = db.Column('student_id', db.Integer, primary_key = True)
    system_public = db.Column(db.String())
    system_private = db.Column(db.String()) 

    def __init__(self, system_public, system_private):
        self.system_public = system_public
        self.system_private = system_private

class peers(db.Model):
    id = db.Column('student_id', db.Integer, primary_key = True)
    system_public = db.Column(db.String())
    system_private = db.Column(db.String()) 

    def __init__(self, system_public, system_private):
        self.system_public = system_public
        self.system_private = system_private

db.create_all()

#Students.query.filter_by(city = ’Hyderabad’).all()

@app.route('/')
def show_all():
   return render_template('show_all.html', students = students.query.all() )
#---------------------------------------------------------------------------#
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
#---------------------------------------------------------------------------#

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

event = threading.Event()

#Nonce = random.randint(100000,1000000)

peerlist = []

newlock = threading.Lock()
udp_server = server.UdpServer(peerlist, newlock)

publicAfile = open('publicA.key', 'r')
APU = publicAfile.read()

privateAkey = open('privateA.key', 'r')
APR = privateAkey.read()

a_n, a_e, a_d = encryptUTIL.readSpecial(APU, APR)
testChain = BlockChain(APU, a_n, a_d)


'''
POST
takes a JSON with one or more transactions and adds the JSON to the
blockchain. Then adds the blockchain and new block to the HTML.
GET
prints the whole current blockchain to the HTML from a specified startvalue
indicated through the URL
'''   
@app.route('/transactions', methods=['POST', 'GET'])
def transactions():
    if(request.method == 'POST'):
        transactions = request.get_json(force=True)['transactions']
        transactionlist = []
        for t in transactions:
            t = Transaction.parseJSON(t)
            transactionlist.append(t)
        testChain.mineblock(transactionlist)

        currBlock = testChain.head
        blocklist = []
        
        while(True):
            blocklist.append(currBlock);
            if (currBlock.nextBlock is None):
                break
            else:
                currBlock = currBlock.nextBlock;
        return render_template('displayblocks.html', genesis=blocklist)
    elif(request.method == 'GET'):
        if(request.args.get('start') == None):
            strvl = 0
        else:
            strvl = int(request.args.get('start'))

        currBlock = testChain.head
        blocklist = []
        while(True):
            if(currBlock.index >= strvl):
                blocklist.append(currBlock);
            if (currBlock.nextBlock is None):
                break
            else:
                currBlock = currBlock.nextBlock
        return render_template('displayblocks.html', genesis=blocklist)

'''
Shows the blockchain but only the block at a specific ID 
that is specified in the URL. Only shows if the block is 
within the range of the blockchain.
'''   
#a method that shows the blockchain but only the block at a specific ID that is given at the route
@app.route('/transactions/<int:ID>')
def retrivespec(ID):
    strvl = ID

    currBlock = testChain.head
    blocklist = []
    
    lastindex = testChain.tail.index;
    if(strvl > lastindex):
        return "Error: Block index does not exist!"
    else:
        while(True):
            if(currBlock.index == strvl):
                blocklist.append(currBlock);
            if (currBlock.nextBlock is None):
                break
            else:
                currBlock = currBlock.nextBlock

    return render_template('displayblocks.html', genesis=blocklist)



publicAfile = open('publicA.key', 'r')
CPU = publicAfile.read()

privateAkey = open('privateA.key', 'r')
CPR = privateAkey.read()

c_n, c_e, c_d = encryptUTIL.readSpecial(CPU, CPR)

MyThread = threading.Thread(target=udp_server.run(event))
MyThread.start()


'''
POST
Peers method receives a post request and decrypts the JSON
that holds a peer's public key and encrypted Nonce
Makes a new peer and adds to peerlist only if it doesnt already exist
Returns with a reincrypted Nonce and its public key.
GET
Returns a list of all known peers through HTML
'''
@app.route('/peers', methods=['POST','GET'])
def peers():
    if(request.method == 'POST'):
        info_json = request.get_json(force=True)
        public_key = info_json['Public Key']
        nonce_signed = info_json['Nonce']
        ip_address = request.remote_addr

        x_n, x_e, x_d = encryptUTIL.readSpecial(public_key, None)

        nonce_decrypted = encryptUTIL.decryptSpecial(x_n, x_e, nonce_signed)

        newpeer = Peer(nonce_decrypted, public_key, ip_address)
        inside = False
        newlock.acquire()
        for n in peerlist:
            if(n.address == newpeer.address):
                inside = True

        if(inside == False):
            peerlist.append(newpeer)
        nonce_reincrypted = encryptUTIL.signSpecial(c_n, c_d, nonce_decrypted)
        returninfo = {}
        returninfo['peerlist'] = []
        for peer in peerlist:
            returninfo['peerlist'].append(peer.toJSON())
        returninfo['nonce'] = nonce_reincrypted
        returninfo['p_key'] = APU

        returninfo = json.dumps(returninfo)
        newlock.release()
        return returninfo
    elif(request.method == 'GET'):
         return render_template('peers.html', peerlist=peerlist)
    return "you connected!"

'''
GET
if mode=json, returns an unecrypted JSON of the peerlist
'''
@app.route('/peers', methods=['GET'])
def getpeers(ID):
    if(request.method == 'GET'):
        if(request.args.get('mode') == None):
            strvl = 'json'
        else:
            strvl = (request.args.get('mode'))
    
        if(strvl == 'json'):
            newJSON = {}
            count = 1
            newlock.acquire()
            for n in peerlist:
                newJSON['peer' + count] = n.toJSON()
                count+= 1
            newlock.release()
            return newJSON

app.run(host='0.0.0.0', port=8001)

signal.signal(signal.SIGINT, signal_handler)
while(True):
    pass
