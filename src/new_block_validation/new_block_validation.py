from common.block import Block


class NewBlockException(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class NewBlock:
    def __init__(self, blockchain: Block):
        self.blockchain = blockchain
        self.new_block = dict()

    def receive(self, new_block: dict):
        self.new_block = new_block

    def validate(self):
        pass

    def add(self):
        pass
