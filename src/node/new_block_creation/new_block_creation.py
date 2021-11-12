import json
from datetime import datetime

from blockchain_users.miner import private_key as miner_private_key
from common.block import Block, BlockHeader
from common.block_reward import BLOCK_REWARD
from common.io_blockchain import get_blockchain_from_memory
from common.io_mem_pool import MemPool
from common.merkle_tree import get_merkle_root
from common.network import Network
from common.owner import Owner
from common.transaction_output import TransactionOutput
from common.utils import calculate_hash
from common.values import NUMBER_OF_LEADING_ZEROS


class BlockException(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class ProofOfWork:
    def __init__(self, network: Network):
        self.network = network
        self.blockchain = get_blockchain_from_memory()
        self.new_block = None
        self.mempool = MemPool()

    @staticmethod
    def get_noonce(block_header: BlockHeader) -> int:
        block_header_hash = ""
        noonce = block_header.noonce
        starting_zeros = "".join([str(0) for _ in range(NUMBER_OF_LEADING_ZEROS)])
        while not block_header_hash.startswith(starting_zeros):
            noonce = noonce + 1
            block_header_content = {
                "previous_block_hash": block_header.previous_block_hash,
                "merkle_root": block_header.merkle_root,
                "timestamp": block_header.timestamp,
                "noonce": noonce
            }
            block_header_hash = calculate_hash(json.dumps(block_header_content))
        return noonce

    def create_new_block(self):
        transactions = self.mempool.get_transactions_from_memory()
        if transactions:
            transaction_fees = self.get_transaction_fees(transactions)
            coinbase_transaction = self.get_coinbase_transaction(transaction_fees)
            transactions.append(coinbase_transaction)
            block_header = BlockHeader(
                merkle_root=get_merkle_root(transactions),
                previous_block_hash=self.blockchain.block_header.hash,
                timestamp=datetime.timestamp(datetime.now()),
                noonce=0
            )
            block_header.noonce = self.get_noonce(block_header)
            block_header.hash = block_header.get_hash()
            self.new_block = Block(transactions=transactions, block_header=block_header)
        else:
            raise BlockException("", "No transaction in mem_pool")

    def get_transaction_fees(self, transactions: list) -> int:
        transaction_fees = 0
        for transaction in transactions:
            input_amount = 0
            output_amount = 0
            for transaction_input in transaction["inputs"]:
                utxo = self.blockchain.get_transaction_from_utxo(transaction_input["transaction_hash"])
                if utxo:
                    utxo_amount = utxo["outputs"][transaction_input["output_index"]]["amount"]
                    input_amount = input_amount + utxo_amount
            for transaction_output in transaction["outputs"]:
                output_amount = output_amount + transaction_output["amount"]
            transaction_fees = transaction_fees + (input_amount-output_amount)
        return transaction_fees

    @staticmethod
    def get_coinbase_transaction(transaction_fees: float) -> dict:
        owner = Owner(private_key=miner_private_key)
        transaction_output = TransactionOutput(
            amount=transaction_fees + BLOCK_REWARD,
            public_key_hash=owner.public_key_hash
        )
        return {"inputs": [],
                "outputs": [transaction_output.to_dict()]}

    def broadcast(self):
        node_list = self.network.known_nodes
        for node in node_list:
            if node.hostname != self.network.node.hostname:
                block_content = {
                    "block": {
                        "header": self.new_block.block_header.to_dict,
                        "transactions": self.new_block.transactions
                    },
                    "sender": self.network.node.hostname
                }
                node.send_new_block(block_content)
