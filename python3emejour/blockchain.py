# -*- coding: iso-8859-15 -*-
from block import Block
from hashlib import sha256
import json

class Blockchain:
    block = []

    def __init__(self):
        pass
    
    def add(self, data):
        index = len(self.block)
        if index > 0:
            previousHash = self.block[index -1].blockHash
        else:
            previousHash = None
        self.block.append(Block().init_block(data, index, previousHash))
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
        else :
            raise ValueError("L'index fourni est en dehors des limites du tableau")
    
    def verify_two_block(self, index_block):
        if index_block > 0 and index_block <= len(self.block) :
            previous_block = self.block[index_block-1]
            current_block = self.block[index_block]

            if previous_block.blockHash == current_block.previousHash:
                previous_content = str(previous_block.index)+ str(previous_block.previousHash)+ str(previous_block.timestamp)+ str(previous_block.data) + str(previous_block.nonce)
                previous_hash = sha256(previous_content.encode('utf-8')).hexdigest()
                
                if str(previous_hash) == str(current_block.previousHash) :
                    print("Les deux block sont conformes")
                    return 1
                else :
                    raise ValueError("Une modification a été opéré dans le contenu d'un des blocks")

            else :
                raise ValueError("Les deux blocks ne se succède pas")
        else :
            raise ValueError("L'index est en dehors des limites du tableau")

    def json_save(self, fileName):
        if ".json" not in fileName :
            fileName += ".json"

        with open(fileName, 'w') as f:
            json.dump(self.json_format(), f, indent = 4, ensure_ascii=False)
        return 1

    def json_read(self, fileName):
        block = Block()

        if ".json" not in fileName :
            fileName += ".json"

        with open(fileName) as json_file:
            data = json.load(json_file)
        
        for index,value in data.items():
            if index == "block":
                values = sorted(value.items())
                for i2, v2 in values:
                    self.block.append(block.create_block(v2))

        return 1
    
    def json_format(self):
        tab = {}
        for info in dir(self):
            if not callable(getattr(self, info)) and not info.startswith("__"):
                if info == "block":
                    tab[info] = {}
                    for oneItem in self[info]:
                        json = oneItem.json_format()
                        tab[info][json['index']] = json
        return tab

    def __str__(self):
        string = "Blockchain: \n\n"
        for info in dir(self):
            if not callable(getattr(self, info)) and not info.startswith("__"):
                if info == "block":
                    myStr = ""
                    for oneBlock in self[info]:
                        
                        string += oneBlock.__str__() +"\n"
        
        return string
        

    def __getitem__(self, item):
        if item == "block":
            return self.block

    def delete_last_block(self):
        lastItem = len(self.block)-1
        self.block.remove(self.block[lastItem])
    
    def delete_blockchain(self):
        lng = len(self.block)
        for i in range(lng):
            cpt = (lng - 1) - i
            self.block.remove(self.block[cpt])

    def delete_number_of_block(self, numberOfBlock):
        lng = len(self.block)
        for i in range(numberOfBlock):
            cpt = (lng - 1) - i
            self.block.remove(self.block[cpt])