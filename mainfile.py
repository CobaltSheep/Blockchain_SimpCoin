import time
import hashlib
import encryptUTIL
import json

"""
Double list class is the framework for the blockchain, which extends it
It has an append class, which adds a node to the list
It has a remove class which removes a node from the list
Has a head and tail which store the first and last nodes in the list
"""


class DoubleList(object):
    head = None
    tail = None

    #adds to the double list
    def append(self, data):
        new_node = Block(data, None, None)
        if self.head is None:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            new_node.next = None
            self.tail.next = new_node
            self.tail = new_node

    #removes from the double list
    def remove(self, node_value):
        current_node = self.head

        while current_node is not None:
            if current_node.data == node_value:
                # if it's not the first element
                if current_node.prev is not None:
                    current_node.prev.next = current_node.next
                    current_node.next.prev = current_node.prev
                else:
                    # otherwise we have no prev (it's None), head is the next one, and prev becomes None
                    self.head = current_node.next
                    current_node.next.prev = None

            current_node = current_node.next

"""
Block object stores transaction lists and is the node of the list.
Index: index of block in list
Nonce: number of leading zeroes of the hash equal to difficulty
Timestamp: UNIX time when block was created
PreviousBlock: stores previous block
NextBlock: stores next block
Merkle: root of merkle tree made by hashing which verifies and stores the order of transactions
CurrentHash: hash of the current block (all of its info)
PrevHash: hash of the previous block
"""
class Block(object):

    #constructor -> sets all values and creates merkle root
    def __init__(self,idx,dt,prevBlock):
        self.index = idx;
        self.data = dt[:BlockChain.translimit];
        self.Nonce = 0;
        self.timestamp = time.time();
        self.previousBlock = prevBlock;
        self.nextBlock = None;
        self.merkle = self.createMerkle(self.data);
        self.currentHash = None;
        if(prevBlock != None):
            self.prevHash = prevBlock.currentHash;
        else:
            self.prevHash = None;

    #creates string version of block
    def __repr__(self):
        string1 = "Index:" + str(self.index) + "-" + "Timestamp:" + str(self.timestamp) + "-" + "Data:" + str(self.data) + "-" + "Previous Hash:" + str(self.prevHash) + "-" + "Nonce:" + str(self.Nonce);
        string15 = "-" + "Current Hash:" + str(self.currentHash);
        return string1 + string15;

    #creates concat hash of all transactions in data
    def returnData(self):
        datastring = "";
        for datapoint in self.data:
            datastring += str(datapoint);
        return datastring;

    #creates hash version of block
    def generateHash(self):
        hashstring = str(self.index) + str(self.timestamp) + self.returnData() + str(self.prevHash) + str(self.Nonce);
        m = hashlib.sha256();
        m.update(hashstring.encode('utf-8'));
        return m.hexdigest();

    #creates merkle root ->assembly of all transactions
    def createMerkle(self, transactionarray):
        tra_queue = [];
        for idx, turtle in enumerate(transactionarray):
            hash = turtle.generateHash();
            tra_queue.append(hash)

        while len(tra_queue) > 0:
            if len(tra_queue) == 1:
                return tra_queue.pop(0);
            else:
                first = tra_queue.pop(0);
                second = tra_queue.pop(0);

                concat = first + second;
                concat = concat.encode();
                y = hashlib.sha256();
                y.update(concat);
                y = y.hexdigest();
                tra_queue.append(y);

        return tra_queue.pop(0);

"""
DestinationId: the public key of the destination of the transaction
OriginatorId: the public key of the sender of the transaction
Addamt: the amount of the transaction in simpcoins
Timestamp: time when the transaction was created (UNIX)
CurrentHash: hash of the information in the transaction (signed by private key of sender)
"""
class Transaction(object):

    #constructor -> sets values and signs hash
    def __init__(self, timestp, dest ,orig, currhash, add, a_n, a_d):
        self.destinationID = dest;
        self.originatorID = orig;
        self.addamt = add;
        if time != None:
            self.timestamp = timestp    
        else:
            self.timestamp = time.time()
            
        if(currhash == None):
            self.currentHash = encryptUTIL.signSpecial(a_n, a_d, self.generateHash())
        else:
            self.currentHash = currhash
        
        

    #checks if amounts are greater than zero
    def verify(self):
        if(self.addamt > 0):
            return True;
        else:
            return False;

    #generates hash of transaction
    def generateHash(self):
        hashstring = str(self.destinationID) + str(self.originatorID) + str(self.addamt) + str(self.timestamp);
        m = hashlib.sha256();
        m.update(hashstring.encode('utf-8'));
        return m.hexdigest();

    @staticmethod
    def parseJSON(dict):

        receiver = dict['recv']
        sender = dict['sender']

        return Transaction(dict['timestamp'], receiver, sender, dict['hash'], dict['amount'], None, None)

"""
Difficulty: number which represents the number of zeroes required for the nonce of each block
Translimit: the limit on the number of transactions in a block
Head: start of blockchain (first block)
Tail: end of blockchain (last block)
"""
class BlockChain(DoubleList):
    difficulty = 2;
    translimit = 256
    def __repr__(self):
        return json.dumps(self, cls=ChainEncoder);

    #constructor for blockchain -> creates genesis block
    def __init__(self, creator_id, a_n, a_d):
        mytransaction = Transaction(None, creator_id, None, None, 100, a_n, a_d);
        list = [];
        list.append(mytransaction)
        genesisBlock = Block(0, list, None);
        genesisBlock.currentHash = genesisBlock.generateHash()
        self.head = genesisBlock;
        self.tail = genesisBlock;

    #verifies chain by checking merkle roots, hashes and previous hashes
    def verifychain(self):
        currentBlock = self.head;
        while currentBlock != None:
            generated = currentBlock.generateHash();
            if currentBlock.currentHash != generated:
                return False
            if(currentBlock != self.tail):
                if currentBlock.nextBlock.prevHash != generated:
                    return False
            if currentBlock.createMerkle(currentBlock.data) != currentBlock.merkle:
                return False;
            for item in currentBlock.data:
                if(item.verify() == False):
                    return False;
            currentBlock = currentBlock.nextBlock;
        return True;

    #checks the balance when given an ID, reads all transactions and calculates total balance
    def checkBalance(self, id):
        currentBlock = self.head;
        currentBalance = 0;
        while(currentBlock != None):
            for idx, element in enumerate(currentBlock.data):
                if(element.originatorID == id):
                    currentAmount = int(element.addamt)
                    currentBalance -= currentAmount;
                else:
                    if(element.destinationID == id):
                        currentAmount = int(element.addamt)
                        currentBalance += currentAmount;
            currentBlock = currentBlock.nextBlock;
        return currentBalance;

    #returns the tail of the blockchain
    def getLatestBlock(self):
        return self.tail;

    #adds a block to the chain with a given array of transactions -> generates a hash with a specific Nonce
    def mineblock(self, transactionArray):
        lb = self.getLatestBlock();
        newBlock = Block(lb.index+1, transactionArray, lb);
        lb.nextBlock = newBlock;
        self.tail = newBlock;
        zeroes = "0"*self.difficulty;
        lhash = newBlock.generateHash();
        while lhash[:self.difficulty] != zeroes:
            newBlock.Nonce += 1;
            lhash = newBlock.generateHash();
        newBlock.currentHash = lhash;


    #creates a string version of the blockchain
    def __repr__(self):
        finished = False;
        currentBlock = (self.head)
        blocks = "";
        while finished == False:
            blocks += blocks + str(currentBlock);
            if (currentBlock.nextBlock == None):
                finished = True;
            else:
                currentBlock = currentBlock.nextBlock;
        return blocks

    #returns the whole block chain in a list
    def returnall(self):
        finished = False;
        currentBlock = (self.head)
        blocks = []
        while finished == False:
            blocks.append(currentBlock)
            if (currentBlock.nextBlock == None):
                finished = True;
            else:
                currentBlock = currentBlock.nextBlock;
        return blocks


if __name__ == '__main__':

    """reading files"""

    print("Reading Pair A...");
    publicAfile = open('publicA.key', 'r');
    APU = publicAfile.read();

    privateAkey = open('privateA.key', 'r');
    APR = privateAkey.read();

    print("Reading Pair B...");
    publicBfile = open('publicB.key', 'r');
    BPU = publicBfile.read();

    privateBfile = open('privateB.key', 'r');
    BPR = publicBfile.read();

    publicCfile = open('publicC.key', 'r');
    CPU = publicCfile.read();

    privateCfile = open('privateC.key', 'r');
    CPR = privateCfile.read();

    a_n, a_e, a_d = encryptUTIL.readSpecial(APU, APR);
    b_n, b_e, b_d = encryptUTIL.readSpecial(BPU, BPR);

    print("Creating BlockChain...");
    testChain = BlockChain(APU, a_n, a_d);


    onelist = [];
    twolist = [];
    threelist = [];
    fourlist = [];
    fivelist = [];

    transaction1 = Transaction(BPU, APU, 40, a_n, a_d);
    transaction2 = Transaction(APU, BPU, 15, b_n, b_d);
    transaction3 = Transaction(BPU, APU, 60, a_n, a_d);
    transaction4 = Transaction(BPU, APU, 20, a_n, a_d);
    transaction5 = Transaction(APU, BPU, 50, b_n, b_d);

    newlist = [];


    onelist.append(transaction1);
    twolist.append(transaction2);
    threelist.append(transaction3);
    fourlist.append(transaction4);
    fivelist.append(transaction5);

    newlist.append(onelist);
    newlist.append(twolist);
    newlist.append(threelist);
    newlist.append(fourlist);
    newlist.append(fivelist);



    count = 0;
    for idx, trarray in enumerate(newlist):
        approvedlist = [];
        for idx2, transaction in enumerate(trarray):
            count = count +1;
            transactionamount = int(transaction.addamt);
            if transaction.originatorID == APU:
                sender = "A";
            else:
                if transaction.originatorID == BPU:
                    sender = "B"
            if transaction.destinationID == APU:
                receiver = "A";
            else:
                if transaction.destinationID == BPU:
                    receiver = "B"

            print("Transaction " + str(count) + " (Amount: " + str(transaction.addamt) + "): " + str(sender) + "->" + str(receiver) + " ", end="");
            senderamount = testChain.checkBalance(transaction.originatorID);
            if senderamount >= transactionamount:
                print("Accepted")
                approvedlist.append(transaction);
            else:
                print("Denied")

        if(len(approvedlist) > 0):
            print("Mining Block " + str(testChain.tail.index + 1) + "... ", end="")
            reward = Transaction(None, CPU, 10, a_n, a_d);
            approvedlist.insert(0, reward);
            testChain.mineblock(approvedlist);
            print("(" + str(testChain.getLatestBlock().Nonce) + "," + str(testChain.getLatestBlock().currentHash) + ")")

    print("Chain Verification... ", end="")
    if(testChain.verifychain() == True):
        print("Verified")
    else:
        print("Not Verified")

    Abalance = testChain.checkBalance(APU);
    Bbalance = testChain.checkBalance(BPU);
    print("Amount in A's Wallet: " + str(Abalance));
    print("Amount in B's Wallet: " + str(Bbalance));
