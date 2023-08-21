from clusters.models import Clusters


class ClusterRunner:
    def __init__(self, cluster: Clusters):
        self.cluster = cluster

    def start(self):
        # Validate status, if we should start at all
        # Change status to starting/running - whatever
        # check how many minions does it have now - introduce Minion model, refresh current state, maybe we should schedule LB config refresh to another task
        # If we are short of minions then spin next one
        # wait a while and start over
        # refresh cluster from DB to check for any updates
        pass
