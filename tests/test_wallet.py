import binascii
import json
import os

import pytest
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15

from utils import convert_transaction_data_to_bytes
from wallet import Transaction, initialize_wallet


def forge_message(transaction_data: bytes) -> bytes:
    transaction_string = transaction_data.decode('utf-8')
    transaction_dict = json.loads(transaction_string)
    transaction_dict["amount"] = 50
    return json.dumps(transaction_dict, indent=2).encode('utf-8')


def cleanup(file_directory: str):
    os.remove(file_directory)


def open_transaction_file(file_directory: str):
    f = open(file_directory, "r")
    file_content = f.read()
    file_dict = json.loads(file_content)
    transaction_data = file_dict["transaction_data"].encode("utf-8")
    transaction_data_dict = json.loads(transaction_data)
    transaction_data_bytes = convert_transaction_data_to_bytes(transaction_data_dict)
    signature_bytes = binascii.unhexlify(file_dict["signature"])
    return transaction_data_bytes, signature_bytes


class TestWallet:

    def test_given_valid_signature_when_signature_is_validated_then_no_exception_is_thrown(self):
        owner = initialize_wallet()
        transaction = Transaction(owner, b'abcd1234', 10)
        file_directory = transaction.sign()
        transaction_data, signature = open_transaction_file(file_directory)
        public_key_object = RSA.import_key(owner.public_key)
        hash = SHA256.new(transaction_data)

        pkcs1_15.new(public_key_object).verify(hash, signature)

        cleanup(file_directory)

    def test_given_non_valid_signature_when_signature_is_validated_then_exception_is_thrown(self):
        owner = initialize_wallet()
        transaction = Transaction(owner, b'abcd1234', 10)
        file_directory = transaction.sign()
        transaction_data, signature = open_transaction_file(file_directory)
        forged_transaction_data = forge_message(transaction_data)
        public_key_object = RSA.import_key(owner.public_key)
        hash = SHA256.new(forged_transaction_data)

        with pytest.raises(Exception):
            pkcs1_15.new(public_key_object).verify(hash, signature)

        cleanup(file_directory)
