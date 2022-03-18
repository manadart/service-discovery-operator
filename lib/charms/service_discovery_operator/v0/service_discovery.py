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
        self._payload_file_name = '/tmp/service-discovery-payload.json'

    def start_discovery(self):
        self.stop_discovery()

        logging.info('Starting discovery process')

        self._charm.payload_file_name = self._payload_file_name

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
                self._charm.charm_dir,
                self._payload_file_name
            ],
            stdout=open('discovery.log', 'a'),
            stderr=subprocess.STDOUT,
            env=new_env
        ).pid

        self._charm.discovery_pid = pid
        logging.info('Discovery process started with PID {}'.format(pid))

    def stop_discovery(self):
        pid = self._charm.discovery_pid
        if not pid:
            return

        try:
            os.kill(pid, signal.SIGINT)
            logging.info('Stopped running discovery process with PID {}'.format(pid))
        except OSError:
            pass


def write_payload(file_name):
    with open(file_name, 'w') as f:
        f.write(str(time.time()))


def dispatch(tools_path, unit, charm_dir):
    dispatch_sub_cmd = 'JUJU_DISPATCH_PATH={}/hooks/discovery {}/dispatch'.format(charm_dir, charm_dir)
    subprocess.run([tools_path, '-u', unit, dispatch_sub_cmd])


def main():
    args = sys.argv[1:]

    tools_path = args[0]
    unit = args[1]
    charm_dir = args[2]
    payload_file_name = args[3]

    while True:
        write_payload(payload_file_name)
        dispatch(tools_path, unit, charm_dir)
        time.sleep(5)


if __name__ == "__main__":
    main()
