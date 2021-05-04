from block import Block

class Blockchain:
    block = []

    def __init__(self, genesisBlock):
        self.block += genesisBlock
    
    def add(self, newBlock):
        self.block += newBlock
