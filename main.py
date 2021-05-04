from block import Block
from blockchain import Blockchain

def main():

    bc = Blockchain("Bonjour")
    bc.add("Hello")
    bc.add("A urevoir")
    bc.add("Pitchoune")

    bc.verify_two_block(1)
    bc.verify_block_content(-1)

    return 1

main()