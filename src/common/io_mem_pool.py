import json


FILENAME = "src/doc/mem_pool"


def get_transactions_from_memory():
    with open(FILENAME, "rb") as file_obj:
        current_mem_pool_str = file_obj.read()
        current_mem_pool_list = json.loads(current_mem_pool_str)
    return current_mem_pool_list


def store_transactions_in_memory(transactions: list):
    text = json.dumps(transactions).encode("utf-8")
    with open(FILENAME, "wb") as file_obj:
        file_obj.write(text)
