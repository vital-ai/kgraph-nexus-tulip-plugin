import os
import sys
from tulip import tlp
import tulipplugins
import requests
from dotenv import load_dotenv
from kgraph_nexus_client import KGraphNexusClient

current_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(current_dir, '.env')
load_dotenv(dotenv_path)


class KGraphNexusSearch(tlp.Algorithm):
    def __init__(self, context):
        tlp.Algorithm.__init__(self, context)

        self.KGRAPH_NEXUS_ENDPOINT = os.getenv('KGRAPH_NEXUS_ENDPOINT')
        self.KGRAPH_NEXUS_PORT = os.getenv('KGRAPH_NEXUS_PORT')

        print(f"KGraphNexusSearch ENDPOINT: {self.KGRAPH_NEXUS_ENDPOINT}", file=sys.stdout)
        print(f"KGraphNexusSearch PORT: {self.KGRAPH_NEXUS_PORT}", file=sys.stdout)

        self.kgraph_nexus_client = KGraphNexusClient(self.KGRAPH_NEXUS_ENDPOINT, self.KGRAPH_NEXUS_PORT)

        status = self.kgraph_nexus_client.status()

        print(f"KGraphNexusSearch Client Status: {status}", file=sys.stdout)
        print("KGraphNexusSearch initialized", file=sys.stdout)

        self.addStringParameter("NodeName", "Name of the node(s) to search for", "")

    def check(self):
        # This method is called before applying the algorithm on the input graph.
        # You can perform some precondition checks here.
        # See comments in the run method to know how to access to the input graph.

        self.pluginProgress.setComment("KGraphNexusSearch Check")

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

        self.pluginProgress.setComment("KGraphNexusSearch Run")

        node_name = self.dataSet["NodeName"]

        # search_string = "happy"

        search_string = node_name

        result_list = self.kgraph_nexus_client.search(search_string)

        graph = self.graph

        label_prop = graph.getStringProperty("viewLabel")

        for item in result_list:

            node = graph.addNode()

            for key, value in item.items():
                # Create or get the property in the graph
                p = graph.getStringProperty(key)
                # Set the property value for the node
                p[node] = str(value)  # Ensure the value is a string

                if key == "http://vital.ai/ontology/vital-core#hasName":
                    label_prop[node] = str(value)

        print("Nodes added to the graph successfully.")

        return True


tulipplugins.registerPluginOfGroup("KGraphNexusSearch", "1. KGraphNexusSearch", "Marc Hadfield", "13/07/2024", "KGraphNexusSearch Info", "0.1.0", "KGraph Query")

