# Contributing

## Building the docker image

```bash
docker login
docker build -t gruyaume/my-blockchain:1.0.0 .
docker push gruyaume/my-blockchain:1.0.0
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
export PYTHONPATH=src
pytest integration_tests
```

Note that you can change the HTTP port that your flask app listens on by adding the `--port` option to `flask run`.
Example: `flask run --port 5002`