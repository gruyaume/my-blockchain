import json

from common.utils import calculate_hash


class BlockHeader:
    def __init__(self, previous_block_hash: str, timestamp: float, noonce: int, merkle_root: str):
        self.previous_block_hash = previous_block_hash
        self.merkle_root = merkle_root
        self.timestamp = timestamp
        self.noonce = noonce
        self.hash = self.get_hash()

    def __eq__(self, other):
        try:
            assert self.previous_block_hash == other.previous_block_hash
            assert self.merkle_root == other.merkle_root
            assert self.timestamp == other.timestamp
            assert self.noonce == other.noonce
            assert self.hash == other.hash
            return True
        except AssertionError:
            return False

    def get_hash(self) -> str:
        header_data = {"previous_block_hash": self.previous_block_hash,
                       "merkle_root": self.merkle_root,
                       "timestamp": self.timestamp,
                       "noonce": self.noonce}
        return calculate_hash(json.dumps(header_data))

    @property
    def to_dict(self) -> dict:
        return {
            "previous_block_hash": self.previous_block_hash,
            "merkle_root": self.merkle_root,
            "timestamp": self.timestamp,
            "noonce": self.noonce,
        }

    def __str__(self):
        return json.dumps(self.to_dict)

    @property
    def to_json(self) -> str:
        return json.dumps(self.to_dict)


class Block:
    def __init__(
            self,
            transactions: [dict],
            block_header: BlockHeader,
            previous_block=None,
    ):
        self.block_header = block_header
        self.transactions = transactions
        self.previous_block = previous_block

    def __eq__(self, other):
        try:
            assert self.block_header == other.block_header
            assert self.transactions == other.transactions
            return True
        except AssertionError:
            return False

    def __len__(self) -> int:
        i = 1
        current_block = self
        while current_block.previous_block:
            i = i + 1
            current_block = current_block.previous_block
        return i

    def __str__(self):
        return json.dumps({"timestamp": self.block_header.timestamp,
                           "hash": self.block_header.hash,
                           "transactions": self.transactions})

    @property
    def to_dict(self):
        block_list = []
        current_block = self
        while current_block:
            block_data = {
                "header": current_block.block_header.to_dict,
                "transactions": current_block.transactions
            }
            block_list.append(block_data)
            current_block = current_block.previous_block
        return block_list

    @property
    def to_json(self) -> str:
        return json.dumps(self.to_dict)

    def get_transaction(self, transaction_hash: dict) -> dict:
        current_block = self
        while current_block.previous_block:
            for transaction in current_block.transactions:
                if transaction["transaction_hash"] == transaction_hash:
                    return transaction
            current_block = current_block.previous_block
        return {}

    def get_user_utxos(self, user: str) -> dict:
        return_dict = {
            "user": user,
            "total": 0,
            "utxos": []
        }
        current_block = self
        while current_block.previous_block:
            for transaction in current_block.transactions:
                for output in transaction["outputs"]:
                    locking_script = output["locking_script"]
                    for element in locking_script.split(" "):
                        if not element.startswith("OP") and element == user:
                            return_dict["total"] = return_dict["total"] + output["amount"]
                            return_dict["utxos"].append(
                                {
                                    "amount": output["amount"],
                                    "transaction_hash": transaction["transaction_hash"]
                                }
                            )
            current_block = current_block.previous_block
        return return_dict

    def get_transaction_from_utxo(self, utxo_hash: str) -> dict:
        current_block = self
        while current_block:
            for transaction in current_block.transactions:
                if utxo_hash == transaction["transaction_hash"]:
                    return transaction
            current_block = current_block.previous_block

    def get_locking_script_from_utxo(self, utxo_hash: str, utxo_index: int):
        transaction_data = self.get_transaction_from_utxo(utxo_hash)
        return transaction_data["outputs"][utxo_index]["locking_script"]
