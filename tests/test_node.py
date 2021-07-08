# from datetime import datetime
#
# import pytest
#
# from block import Block
# from utils import generate_transaction_data
#
#
# class TestNode:
#
#     @pytest.fixture(scope="module")
#     def blockchain(self):
#         timestamp_0 = datetime.timestamp(datetime.fromisoformat('2011-11-04 00:05:23.111'))
#         transaction_data_0 = generate_transaction_data(b'Albert', b'Bertrand', 30)
#         block_0 = Block(
#             transaction_data=transaction_data_0,
#             timestamp=timestamp_0
#         )
#
#         timestamp_1 = datetime.timestamp(datetime.fromisoformat('2011-11-07 00:05:13.222'))
#         transaction_data_1 = generate_transaction_data(b'Albert', b'Camille', 10)
#         block_1 = Block(
#             transaction_data=transaction_data_1,
#             timestamp=timestamp_1,
#             previous_block=block_0
#         )
#
#         timestamp_2 = datetime.timestamp(datetime.fromisoformat('2011-11-09 00:11:13.333'))
#         transaction_data_2 = generate_transaction_data(b'Bertrand', b'Camille', 5)
#         block_2 = Block(
#             transaction_data=transaction_data_2,
#             timestamp=timestamp_2,
#             previous_block=block_1
#         )
#         return block_2
#
#     def test_given_sufficient_funds_when_validate_funds_then_return_true(self, blockchain):
#         print(blockchain.timestamp)
#         pass
#
#     def test_given_insufficient_funds_when_validate_funds_then_return_false(self):
#         pass
