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
import time

from ops.charm import CharmBase
from ops.framework import StoredState
from ops.main import main
from ops.model import ActiveStatus
from charms.service_discovery_operator.v0.event import DiscoveryEventCharmEvents
from charms.service_discovery_operator.v0.service_discovery import ServiceDiscovery

logger = logging.getLogger(__name__)


class ServiceDiscoveryCharm(CharmBase):
    """Charm the service."""

    on = DiscoveryEventCharmEvents()
    _stored = StoredState()

    def __init__(self, *args):
        super().__init__(*args)

        self._stored.set_default(discovery_pid=None)
        self._stored.set_default(discovery_payload=None)

        self._service_discovery = ServiceDiscovery(self)

        self.framework.observe(self.on.start, self._on_start)
        self.framework.observe(self.on.discovery, self._on_discovery)
        self.framework.observe(self.on.leader_elected, self._on_leader_elected)

    def _on_start(self, event):
        self.unit.status = ActiveStatus()

    def _on_leader_elected(self, event):
        if self.unit.is_leader():
            self._service_discovery.start_discovery()
        else:
            self._service_discovery.stop_discovery()

    def _on_discovery(self, event):
        self.unit.status = ActiveStatus(self._read_discovery_payload())

    def _read_discovery_payload(self):
        with open(self.payload_file_name, 'r') as f:
            return f.read()

    @property
    def unit_tag(self):
        unit_num = self.unit.name.split("/")[-1]
        return "unit-{}-{}".format(self.app.name, unit_num)

    @property
    def discovery_pid(self):
        return self._stored.discovery_pid

    @discovery_pid.setter
    def discovery_pid(self, pid):
        self._stored.discovery_pid = pid

    @property
    def payload_file_name(self):
        return self._stored.payload_file_name

    @payload_file_name.setter
    def payload_file_name(self, file_name):
        self._stored.payload_file_name = file_name


if __name__ == "__main__":
    main(ServiceDiscoveryCharm)
