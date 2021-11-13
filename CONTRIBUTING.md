# Contributing

## Building the docker images

```bash
docker login
docker build -t gruyaume/my-blockchain:1.0.0 -f node.Dockerfile .
docker build -t gruyaume/my-miner:1.0.0 -f miner.Dockerfile .
docker push gruyaume/my-blockchain:1.0.0
docker push gruyaume/my-miner:1.0.0
```


## Unit tests
Run unit tests locally by running the following:
```bash
pip3 install tox
tox -e unit
```

## Integration tests
Integration tests allow to complete transactions from the wallet to the node.

Run integration tests:
```bash
pip3 install tox
tox -e integration
```
