from common.owner import Owner

owner = Owner()
print(f"private key: {owner.private_key.export_key(format='DER')}")
print(f"public key hash: {owner.public_key_hash}")
print(f"public key hex: {owner.public_key_hex}")
