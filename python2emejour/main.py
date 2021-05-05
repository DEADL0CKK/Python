from block import Block
from blockchain import Blockchain

def main():

    bc = Blockchain()
    # bc.add("Bonjour")
    # bc.add("Hello")
    # bc.add("A urevoir")
    # bc.add("Pitchoune")


    # print(bc)
    
    # bc.json_save()
    bc.json_read("data.json")


    bc.verify_block_content(3)
    bc.verify_two_block(1)
    bc.delete_number_of_block(2)
    print(bc)
    return 1


main()