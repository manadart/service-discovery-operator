from ops.framework import EventBase, EventSource
from ops.charm import CharmEvents


class DiscoveryEvent(EventBase):
    pass


class DiscoveryEventCharmEvents(CharmEvents):
    discovery = EventSource(DiscoveryEvent)
