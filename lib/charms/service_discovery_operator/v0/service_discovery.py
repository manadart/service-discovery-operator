import logging
import os
import subprocess
import sys
import time

from ops.framework import Object

logger = logging.getLogger(__name__)


class ServiceDiscovery(Object):

    def __init__(self, charm):
        logging.info('Starting discovery process')

        # We need to trick Juju into thinking that we are not running in a hook
        # context, as Juju will disallow use of juju-run.
        new_env = os.environ.copy()
        new_env.pop("JUJU_CONTEXT_ID")

        pid = subprocess.Popen(
            [
                '/usr/bin/python3',
                'lib/charms/service_discovery_operator/v0/service_discovery.py',
                '/var/lib/juju/tools/unit-service-discovery-0/juju-run',
                charm.unit.name,
                charm.charm_dir
            ],
            stdout=open('discovery.log', 'a'),
            stderr=subprocess.STDOUT,
            env=new_env
        ).pid

        logging.info('Discovery process started with PID {}'.format(pid))


def main():
    args = sys.argv[1:]

    tools_path = args[0]
    unit = args[1]
    charm_dir = args[2]

    while True:
        subprocess.run(
            [
                tools_path,
                '-u',
                unit,
                'JUJU_DISPATCH_PATH={}/hooks/discovery {}/dispatch'.format(charm_dir, charm_dir)
            ]
        )
        time.sleep(5)


if __name__ == "__main__":
    main()
