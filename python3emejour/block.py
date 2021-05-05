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

    def __init__(self):
        pass

    def init_block(self, data, index, previousHash):
        self.index = index
        self.data = data
        self.timestamp = datetime.today().strftime('%Y-%m-%d::%H-%M')                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
        if(previousHash == None):
            self.previousHash = None
        else:
            self.previousHash = previousHash
        self.nonce = 0
        self.calculHash()
        return self

    def create_block(self, data_dict):
        newBlock = Block()
        newBlock.data =  data_dict['data']
        newBlock.index = data_dict['index']
        newBlock.previousHash = data_dict['previousHash']
        newBlock.timestamp = data_dict['timestamp']
        newBlock.nonce = data_dict['nonce']

        block_info = str(newBlock.index)+ str(newBlock.previousHash)+ str(newBlock.timestamp)+ str(newBlock.data) + str(newBlock.nonce)
        block_hash = sha256(block_info.encode('utf-8')).hexdigest()
        if block_hash == data_dict['blockHash'] :
            newBlock.blockHash = data_dict['blockHash']
        else :
            raise Exception("Data fournies corrompues")

        return newBlock

    def calculHash(self):
        while self.blockHash[0:4] != "0000":
            self.nonce += 1
            block = str(self.index)+ str(self.previousHash)+ str(self.timestamp)+ str(self.data) + str(self.nonce)
            self.blockHash = sha256(block.encode('utf-8')).hexdigest()
            
    
    def json_format(self):
        tab = {}
        for info in dir(self):
            if not callable(getattr(self, info)) and not info.startswith("__"):
                tab[info] = self[info]
        return tab

    def __str__(self):
        string = "Block:\n"
        for info in dir(self):
            if not callable(getattr(self, info)) and not info.startswith("__"):
                string += str(info) + ": " + str(self[info]) + "\n"
        return string

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