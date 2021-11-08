#!/usr/bin/env python3
# Copyright 2021 Guillaume
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/sdk

"""Charm the service.

Refer to the following post for a quick-start guide that will help you
develop a new k8s charm using the Operator Framework:

    https://discourse.charmhub.io/t/4208
"""

import logging

from ops.charm import CharmBase
from ops.main import main
from ops.model import ActiveStatus, MaintenanceStatus
from ops.pebble import Layer

logger = logging.getLogger(__name__)


class MyBlockchainCharm(CharmBase):
    """Charm the service."""

    def __init__(self, *args):
        super().__init__(*args)
        self._service_name = self._container_name = "my_blockchain"
        self._container = self.unit.get_container(self._container_name)
        self.framework.observe(self.on.my_blockchain_pebble_ready, self._on_my_blockchain_pebble_ready)

    def _on_my_blockchain_pebble_ready(self, event):
        self.unit.status = MaintenanceStatus("Configuring pod")
        plan = self._container.get_plan()
        layer = self._pebble_layer()
        if plan.services != layer.services:
            self._container.add_layer(self._container_name, layer, combine=True)
            self._container.restart(self._service_name)
            logger.info(f"Restarted container {self._service_name}")
        self.unit.status = ActiveStatus()

    def _pebble_layer(self):
        return Layer(
            {
                "summary": f"{self._service_name} layer",
                "description": f"pebble config layer for {self._service_name}",
                "services": {
                    self._service_name: {
                        "override": "replace",
                        "summary": self._service_name,
                        "command": "flask run",
                        "startup": "enabled",
                    }
                },
            }
        )


if __name__ == "__main__":
    main(MyBlockchainCharm)
