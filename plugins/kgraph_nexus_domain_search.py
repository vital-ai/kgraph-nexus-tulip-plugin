import os
from tulip import tlp
import tulipplugins
import requests
from dotenv import load_dotenv
from kgraph_nexus_client import KGraphNexusClient


current_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(current_dir, '.env')
load_dotenv(dotenv_path)


class KGraphNexusDomainSearch(tlp.Algorithm):
    def __init__(self, context):
        tlp.Algorithm.__init__(self, context)

        self.KGRAPH_NEXUS_ENDPOINT = os.getenv('KGRAPH_NEXUS_ENDPOINT')
        self.KGRAPH_NEXUS_PORT = os.getenv('KGRAPH_NEXUS_PORT')

        print(f"KGraphNexusDomainSearch ENDPOINT: {self.KGRAPH_NEXUS_ENDPOINT}", file=sys.stdout)
        print(f"KGraphNexusDomainSearch PORT: {self.KGRAPH_NEXUS_PORT}", file=sys.stdout)

        self.addStringParameter("NodeName", "Name of the node(s) to search for", "")

        self.kgraph_nexus_client = KGraphNexusClient(self.KGRAPH_NEXUS_ENDPOINT, self.KGRAPH_NEXUS_PORT)

    def check(self):
        # This method is called before applying the algorithm on the input graph.
        # You can perform some precondition checks here.
        # See comments in the run method to know how to access to the input graph.

        # Must return a tuple (Boolean, string). First member indicates if the algorithm can be applied
        # and the second one can be used to provide an error message
        return True, "Ok"

    def run(self):
        # This method is the entry point of the algorithm when it is called
        # and must contain its implementation.

        # The graph on which the algorithm is applied can be accessed through
        # the "graph" class attribute (see documentation of class tlp.Graph).

        # The parameters provided by the user are stored in a dictionary
        # that can be accessed through the "dataSet" class attribute.

        # The method must return a Boolean indicating if the algorithm
        # has been successfully applied on the input graph.

        # node_name = self.dataSet["Node Name"]
        # include_connections = self.dataSet["Include Connections"]
        # distance_metric = self.dataSet["Distance Metric"]

        return True


tulipplugins.registerPluginOfGroup("KGraphNexusDomainSearch", "2. KGraphNexusDomainSearch", "Marc Hadfield", "13/07/2024", "KGraphNexusDomainSearch Info", "0.1.0", "KGraph Query")

