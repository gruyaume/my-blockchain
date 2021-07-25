from flask import Flask, request

from common.initialize_blockchain import blockchain
from new_block_validation.new_block_validation import NewBlock, NewBlockException

app = Flask(__name__)

blockchain_base = blockchain()


@app.route("/block", methods=['POST'])
def validate_block():
    content = request.json
    try:
        new_block = NewBlock(blockchain_base)
        new_block.receive(new_block=content["block"])
        new_block.validate()
        new_block.add()
    except NewBlockException as new_block_exception:
        return f'{new_block_exception}', 400
    return "Transaction success", 200
