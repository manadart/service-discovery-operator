import logging
import os
import signal
import subprocess
import sys
import time

from ops.framework import Object

logger = logging.getLogger(__name__)


class ServiceDiscovery(Object):

    def __init__(self, charm):
        self._charm = charm
        self._stop_existing_discovery()
        self._start_discovery()

    def _stop_existing_discovery(self):
        pid = self._charm.discovery_pid
        if not pid:
            return

        try:
            os.kill(pid, signal.SIGINT)
        except OSError:
            pass

        logging.info('Stopped running discovery process with PID {}'.format(pid))

    def _start_discovery(self):
        logging.info('Starting discovery process')

        # We need to trick Juju into thinking that we are not running in a hook
        # context, as Juju will disallow use of juju-run.
        new_env = os.environ.copy()
        new_env.pop("JUJU_CONTEXT_ID")

        pid = subprocess.Popen(
            [
                '/usr/bin/python3',
                'lib/charms/service_discovery_operator/v0/service_discovery.py',
                '/var/lib/juju/tools/{}/juju-run'.format(self._charm.unit_tag),
                self._charm.unit.name,
                self._charm.charm_dir
            ],
            stdout=open('discovery.log', 'a'),
            stderr=subprocess.STDOUT,
            env=new_env
        ).pid

        logging.info('Discovery process started with PID {}'.format(pid))
        self._charm.discovery_pid = pid


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
