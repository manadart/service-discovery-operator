#!/usr/bin/env python3
# Copyright 2022 joseph
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
from ops.framework import StoredState
from ops.main import main
from ops.model import ActiveStatus
from charms.service_discovery_operator.v0.event import DiscoveryEventCharmEvents

logger = logging.getLogger(__name__)


class ServiceDiscoveryCharm(CharmBase):
    """Charm the service."""

    on = DiscoveryEventCharmEvents()
    _stored = StoredState()

    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.discovery, self._on_discovery)

    def _on_discovery(self, event):
        self.unit.status = ActiveStatus("I got a custom event")


if __name__ == "__main__":
    main(ServiceDiscoveryCharm)
