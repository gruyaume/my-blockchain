# my-blockchain

## Description
My-blockchain is an educational blockchain project. You can find the complete tutorial on 
[medium](https://medium.com).

## Table of contents
0. [Introduction](https://gruyaume.medium.com/create-your-own-blockchain-using-python-4efde6721267)
1. [The basics](https://gruyaume.medium.com/create-your-own-blockchain-using-python-d1250733ce5e)
2. [Merkle tree](https://gruyaume.medium.com/create-your-own-blockchain-using-python-merkle-tree-pt-2-f84478a30690)
3. [Transactions and security](https://gruyaume.medium.com/create-your-own-blockchain-using-python-transactions-and-security-pt-3-407e75d71acf)
4. [Double-entry bookkeeping and UTXO’s](https://gruyaume.medium.com/create-your-own-blockchain-using-python-double-entry-bookkeeping-and-transaction-fees-pt-4-1e399a9cc092)
5. [Transaction scripts](https://gruyaume.medium.com/create-your-own-blockchain-using-python-pt-5-d90cff185380)
6. [The network](https://gruyaume.medium.com/create-your-own-blockchain-using-python-pt-6-d00e06c1c9db)
7. [New Block Creation and Proof-of-Work](https://gruyaume.medium.com/create-your-own-blockchain-using-python-pt-7-6cdcb44697fe)
8. [Incentives and Transaction fees](https://gruyaume.medium.com/create-your-own-blockchain-using-python-pt-8-bf33e01f7cbb)
9. [A Distributed Network](https://gruyaume.medium.com/create-your-own-blockchain-using-python-pt-9-240698fe513b)


## Usage

**my-blockchain** can be deployed via Juju command line using below commands:

```bash
deploy ./my-blockchain_ubuntu-20.04-amd64.charm --resource my-blockchain-image=gruyaume/my-blockchain:1.0.0
```

Before running any **juju deploy** commands, make sure charm has been built using:
```bash
charmcraft pack
```

## OCI Images

Default: gruyaume/my-blockchain:1.0.0
