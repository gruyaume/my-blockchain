from pytest import fixture

from common.block import Block, BlockHeader
from common.io_mem_pool import store_transactions_in_memory
from common.network import Network
from common.node import Node
from node.transaction_validation.transaction_validation import Transaction


class TestTransaction:

    @fixture(scope="module")
    def network(self):
        node = Node("1.1.1.1:1234")
        return Network(node)

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
            self, network, blockchain_base):

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
        transaction = Transaction(blockchain_base, network)
        transaction.receive(transaction=new_transaction)

        assert transaction.is_new

    def test_given_already_stored_transaction_when_is_new_then_returns_false(
            self, network, blockchain_base):
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
        store_transactions_in_memory([new_transaction])

        transaction = Transaction(blockchain_base, network)
        transaction.receive(transaction=new_transaction)

        assert not transaction.is_new
