from node.utils import calculate_hash, convert_transaction_data_to_bytes


def generate_transaction_data(inputs: list, outputs: list) -> dict:
    transaction_data = {
        "inputs": inputs,
        "outputs": outputs,
    }
    transaction_data["hash"] = calculate_hash(convert_transaction_data_to_bytes(transaction_data))
    return transaction_data
