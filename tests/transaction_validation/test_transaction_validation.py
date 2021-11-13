from pytest import fixture

from common.block import Block, BlockHeader
from common.io_blockchain import BlockchainMemory
from common.io_known_nodes import KnownNodesMemory
from common.io_mem_pool import MemPool
from common.network import Network
from common.node import Node
from node.transaction_validation.transaction_validation import Transaction


class TestTransaction:

    @fixture(scope="module")
    def blockchain_memory(self):
        return BlockchainMemory("src/doc/blockchain")

    @fixture(scope="module")
    def known_nodes_memory(self):
        return KnownNodesMemory("src/doc/known_nodes.json")

    @fixture(scope="module")
    def mempool(self):
        return MemPool("src/doc/mem_pool")

    @fixture(scope="module")
    def network(self, blockchain_memory, known_nodes_memory):
        node = Node("1.1.1.1:1234")
        return Network(node, blockchain_memory, known_nodes_memory)

    @fixture(scope="module")
    def blockchain_base(self):
        previous_block_hash = "aaaa"
        merkle_root = "1234"
        timestamp = 111
        noonce = 22
        block_header = BlockHeader(
            merkle_root=merkle_root,
            previous_block_hash=previous_block_hash,
            timestamp=timestamp,
            noonce=noonce
        )
        transactions = []
        return Block(block_header=block_header, transactions=transactions)

    def test_given_new_transaction_when_is_new_then_returns_true(
            self, network, blockchain_base, mempool):

        new_transaction = {
            "inputs": [
                {
                    "whatever key": "whatever value"
                }
            ],
            "outputs": [
                {
                    "whatever key": "whatever value"
                }
            ]
        }
        transaction = Transaction(blockchain_base, network, mempool)
        transaction.receive(transaction=new_transaction)

        assert transaction.is_new

    def test_given_already_stored_transaction_when_is_new_then_returns_false(
            self, network, blockchain_base, mempool):
        new_transaction = {
            "inputs": [
                {
                    "whatever key": "whatever value"
                }
            ],
            "outputs": [
                {
                    "whatever key": "whatever value"
                }
            ]
        }
        mempool.store_transactions_in_memory([new_transaction])

        transaction = Transaction(blockchain_base, network, mempool)
        transaction.receive(transaction=new_transaction)

        assert not transaction.is_new
