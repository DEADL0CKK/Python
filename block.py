from datetime import datetime
import hashlib
import re

class Block:
    index = 0
    blockHash = ""
    previousHash = ""
    timestamp = 0
    nonce = 0
    data = ""

    def __init__(self, data, index, previousHash):
        self.index = index
        self.data = data
        self.timestamp = datetime.timestamp(datetime.now())
        if(previousHash == ""):
            self.previousHash = "None"
        else:
            self.previousHash = previousHash
        self.nonce = 0
        self.calculHash()

    def calculHash(self):
        while(re.search('^....', self.blockHash) != "0000"):
            block = str(self.index)+ str(self.previousHash)+ str(self.timestamp)+ str(self.data) + str(self.nonce)
            self.blockHash = sha256(block.encode('utf-8')).hexdigest()
            self.nonce += 1
    