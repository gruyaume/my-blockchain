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
10. [Publishing and testing](https://gruyaume.medium.com/create-your-own-blockchain-using-python-pt-10-824e6af111f8)

## Requirements

### Python version
Python 3.8

### Libraries
Install libraries with pip:
`pip3 install -r requirements.txt`

### Hardware

- Processor: 2 vCPU
- Memory: 4GB
- Storage: 50GB

## Installation Guide

A complete installation guide is available on Medium (pt. 10). You should be following this guide 
if you want your block to be part of the network and be accessible from the outside world.
Here we will simply deploy the node on a virtual machine without any other infrastructure 
consideration. We will also assume you have access to a virtual machine running Ubuntu 20.04. 
We will install Kubernetes on this VM and deploy our application on it.

### Setting up Microk8s
We will be using [Microk8s](https://microk8s.io/docs), which is a 
free, fast and easy to deploy Kubernetes release. Once you're inside the virtual machine, install 
microk8s using snap:

```bash
ubuntu@ip-10-0-0-54:~$ sudo apt-get update && sudo apt-get upgrade
ubuntu@ip-10-0-0-54:~$ sudo snap install microk8s --classic
```

Update your user's permission to be added to the microk8s group:
```bash
ubuntu@ip-10-0-0-54:~$ sudo usermod -a -G microk8s ubuntu
ubuntu@ip-10-0-0-54:~$ sudo chown -f -R ubuntu ~/.kube
```

After changing those permissions, you'll have to create a new shell for them to take effect, so you 
can exit and re-ssh to the machine. Once you're in again, enable some add-ons to your microk8s cluster:
```bash
ubuntu@ip-10-0-0-54:~$ microk8s enable dns ingress storage
```

We will be using MetalLB as our load balancer for Kubernetes. It can be enabled the same way as the other add-ons:
```bash
ubuntu@ip-10-0-0-54:~$ microk8s enable metallb
```

You will be asked for a range of IP's to provide, answer with the range of private addresses you want, here I'll use : `10.0.1.1–10.0.1.254`.


### Deploying our node using kubectl
MicroK8s uses a namespaced kubectl command to prevent conflicts with any existing installs of kubectl. In our case, we don't have an existing install so we will add an alias like this:

```bash
ubuntu@ip-10-0-0-54:~$ alias kubectl='microk8s kubectl'
```

Note that this alias won't survive exiting your shell session so you'll have to re-run the command every time you log back in. Now clone the code from the github and head to the deploy directory:
```bash
ubuntu@ip-10-0-0-54:~$ git clone https://github.com/gruyaume/my-blockchain.git
ubuntu@ip-10-0-0-54:~$ cd my-blockchain/deploy/
```

Deploy the blockchain using kubectl apply:
```bash
ubuntu@ip-10-0-0-54:~/my-blockchain/deploy$ kubectl apply -f kubernetes/
```

Voilà, you now have a node running.

### Validating the Kubernetes deployment
You can validate that our service is correctly created:
```bash
ubuntu@ip-10-0-0-54:~$ kubectl get svc
NAME            TYPE           CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE
kubernetes      ClusterIP      10.152.183.1     <none>        443/TCP        22m
my-blockchain   LoadBalancer   10.152.183.158   10.0.1.1      80:32301/TCP   20m
```

And that our deployment is also up:

```bash
ubuntu@ip-10-0-0-54:~$ kubectl get pods
NAME                            READY   STATUS    RESTARTS   AGE
my-blockchain-b9d844446-9hnzg   1/1     Running   0          21m
```

### Validating Networking
Still from inside the virtual machine, validate that our service returns something when we call it. 
Here the IP is the EXTERNAL-IP associated to the my-blockchain service. Make sure you use the correct one:

```bash
ubuntu@ip-10-0-0-54:~$ curl 10.0.1.1/block
```

You should get in return the blockchain in a list format.

## New blockchain user 
In the current implementation there are 4 users of the blockchain: albert, bertrand, camille and the miner. To create a 
new user, you will have to generate a new public/private key pair. To do so, you can simply run the 
"new_user_creation.py" script inside of the `common` directory:
```bash
export PYTHONPATH=src
python src/common/new_user_creation.py 
```
The output will simply print you new public/private keys that you will be able to use.
