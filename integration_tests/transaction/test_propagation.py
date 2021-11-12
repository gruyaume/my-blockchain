# import time
#
# import pytest
#
# from blockchain_users.camille import private_key as camille_private_key
# from common.node import Node
# from common.transaction_input import TransactionInput
# from common.transaction_output import TransactionOutput
# from integration_tests.common.default_values import SERVER_HOSTNAME
# from integration_tests.common.flask import Server
# from wallet.wallet import Owner, Wallet
#
#
# @pytest.fixture(scope="module")
# def default_node():
#     return Node(SERVER_HOSTNAME)
#
# @pytest.fixture(scope="module")
# def camille():
#     return Owner(private_key=camille_private_key)
#
#
# @pytest.fixture(scope="module")
# def camille_wallet(camille, default_node):
#     return Wallet(camille, default_node)
#
#
# @pytest.fixture(scope="module")
# def server() -> Server:
#     server = Server()
#     return server
#
#
# def test_given_user_has_funds_when_process_transaction_then_transaction_is_accepted(
#         camille_wallet):
#     server.start()
#     server.stop()
