# Create your own blockchain using Python
The goal of this project is to provide code to support a tutorial on blockchains. You can find the complete tutorial on 
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
10. [Deployment](https://)

## Requirements

### Python version
Python 3.8

### Libraries
Install libraries with pip:
`pip3 install -r requirements.txt`

## Deployment

A docker image is provided on docker hub [here](https://hub.docker.com/repository/docker/gruyaume/my-blockchain). 
The assumption is that you have access to a Kubernetes cluster. 

### Deploying via kubernetes yaml files

Go to the kubernetes deployment directory:

```bash
ubuntu@ip-172-31-24-207:~$ cd my-blockchain/deploy/kubernetes/
```

Create a namespace:
```bash
ubuntu@ip-172-31-24-207:~/my-blockchain/deploy/kubernetes$ kubectl create namespace dev1
```

Deploy the blockchain application:
```bash
ubuntu@ip-172-31-24-207:~/my-blockchain/deploy/kubernetes$ kubectl apply -f my_blockchain_pod.yaml -n dev1
```

### Validation

Use `docker ps` to validate that all 3 nodes are deployed properly.
```bash
(venv) guillaume@thinkpad:~/PycharmProjects/my-blockchain$ docker ps
CONTAINER ID   IMAGE                          COMMAND                  CREATED              STATUS              PORTS                                       NAMES
80792eb022c6   gruyaume/my-blockchain:1.0.0   "python3 -m flask ru…"   4 seconds ago        Up 3 seconds        0.0.0.0:5002->5000/tcp, :::5002->5000/tcp   my-blockchain-2
76cd1174e69b   gruyaume/my-blockchain:1.0.0   "python3 -m flask ru…"   About a minute ago   Up About a minute   0.0.0.0:5001->5000/tcp, :::5001->5000/tcp   my-blockchain-1
86bdd89ab634   gruyaume/my-blockchain:1.0.0   "python3 -m flask ru…"   About a minute ago   Up About a minute   0.0.0.0:5000->5000/tcp, :::5000->5000/tcp   my-blockchain-0
```

You can use Postman to query `http://127.0.0.1:5000/block` (as well as ports `5001` and `5002`) and
you should be receiving an answer in all cases.


## New blockchain user 
In the current implementation there are 4 users of the blockchain: albert, bertrand, camille and the miner. To create a 
new user, you will have to generate a new public/private key pair. To do so, you can simply run the 
"new_user_creation.py" script inside of the `common` directory:
```bash
export PYTHONPATH=src
python src/common/new_user_creation.py 
```
The output will simply print you new public/private keys that you will be able to use.
