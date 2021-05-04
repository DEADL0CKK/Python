# -*- coding: iso-8859-15 -*-
from block import Block
from hashlib import sha256

class Blockchain:
    block = []

    def __init__(self, data):
        index = len(self.block)
        previousHash = None
        self.block.append(Block(data, index, previousHash))
    
    def add(self, data):
        index = len(self.block)
        if index > 0:
            previousHash = self.block[index -1].blockHash
        else:
            previousHash = None
        self.block.append(Block(data, index, previousHash))
        return 1


    def verify_block_content(self, index_block):
        start_correct = 0
        block_info = ""
        block_hash = ""

        if index_block > 0 and index_block <= len(self.block):
            this_block = self.block[index_block]

            if this_block.blockHash[0:4] == "0000":
                start_correct = 1

            if start_correct == 1 :
                block_info = str(this_block.index)+ str(this_block.previousHash)+ str(this_block.timestamp)+ str(this_block.data) + str(this_block.nonce)
                block_hash = sha256(block_info.encode('utf-8')).hexdigest()

            if block_hash == this_block.blockHash :
                print("La contenu du block est valid")
                return 1
            else :
                raise ValueError("Le contenu du block n'est pas valid")
                return -1
        else :
            raise ValueError("L'index fourni est en dehors des limites du tableau")
    
    def verify_two_block(self, index_block):
        if index_block > 0 and index_block <= len(self.block) :
            previous_block = self.block[index_block-1]
            current_block = self.block[index_block]

            if previous_block.blockHash == current_block.previousHash:
                previous_content = str(previous_block.index)+ str(previous_block.previousHash)+ str(previous_block.timestamp)+ str(previous_block.data) + str(previous_block.nonce)
                previous_hash = sha256(previous_content.encode('utf-8')).hexdigest()
                current_content = current_block.previousHash
                if str(previous_hash) == str(current_block.previousHash) :
                    print("Les deux block sont conformes")
                    return 1
                else :
                    raise ValueError("Une modification a été opéré dans le contenu d'un des blocks")
                    return -1

            else :
                raise ValueError("Les deux blocks ne se succède pas")
                return -1
        else :
            raise ValueError("L'index est en dehors des limites du tableau")
            return 0
    
    def __str__(self):
        tab = {}
        for info in dir(self):
            if not callable(getattr(self, info)) and not info.startswith("__"):
                if info == "block":
                    myStr = ""
                    for oneBlock in self[info]:
                        myStr += " , " + oneBlock.__str__()
                    tab[info] = myStr
        
        return str(tab)
        

    def __getitem__(self, item):
        if item == "block":
            return self.block