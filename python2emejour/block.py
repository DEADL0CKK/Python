from datetime import datetime
from hashlib import sha256
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
        self.timestamp = datetime.now()
        if(previousHash == None):
            self.previousHash = None
        else:
            self.previousHash = previousHash
        self.nonce = 0
        self.calculHash()

    def calculHash(self):
        while self.blockHash[0:4] != "0000":
            self.nonce += 1
            block = str(self.index)+ str(self.previousHash)+ str(self.timestamp)+ str(self.data) + str(self.nonce)
            self.blockHash = sha256(block.encode('utf-8')).hexdigest()
            
    
    def __str__(self):
        tab = {}
        for info in dir(self):
            if not callable(getattr(self, info)) and not info.startswith("__"):
                tab[info] = self[info]
        return str(tab)

    def __getitem__(self, item):
        if item == "index":
            return self.index
        elif item == "blockHash":
            return self.blockHash
        elif item == "previousHash":
            return self.previousHash
        elif item == "timestamp":
            return self.timestamp
        elif item == "nonce":
            return self.nonce
        elif item == "data":
            return self.data
        