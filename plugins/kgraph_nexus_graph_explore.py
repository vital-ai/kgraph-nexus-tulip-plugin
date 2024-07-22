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


class KGraphNexusGraphExplore(tlp.Algorithm):
    def __init__(self, context):
        tlp.Algorithm.__init__(self, context)

        self.KGRAPH_NEXUS_ENDPOINT = os.getenv('KGRAPH_NEXUS_ENDPOINT')
        self.KGRAPH_NEXUS_PORT = os.getenv('KGRAPH_NEXUS_PORT')

        print(f"KGraphNexusGraphExplore ENDPOINT: {self.KGRAPH_NEXUS_ENDPOINT}", file=sys.stdout)
        print(f"KGraphNexusGraphExplore PORT: {self.KGRAPH_NEXUS_PORT}", file=sys.stdout)

        self.addBooleanParameter("IncludeConnections", "Include connecting edges/nodes", "true")

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

        graph = self.graph

        uri_prop = graph.getStringProperty("URI")
        label_prop = graph.getStringProperty("viewLabel")

        selected_nodes = []

        view_selection = graph.getBooleanProperty("viewSelection")

        uri_list = []

        for node in graph.getNodes():
            if view_selection[node]:
                selected_nodes.append(node)
                if uri_prop[node]:
                    uri_list.append(uri_prop[node])

        result_list = self.kgraph_nexus_client.graph_explore(uri_list)

        uri_to_node = {}

        for item in result_list:
            if 'http://vital.ai/ontology/vital-core#hasEdgeSource' in item or 'http://vital.ai/ontology/vital-core#hasEdgeDestination' in item:
                # This item is an edge, skip for now
                continue

            node_uri = item.get('URI')
            if not node_uri:
                continue

            node_exists = False
            for n in graph.getNodes():
                if uri_prop[n] == node_uri:
                    node_exists = True
                    uri_to_node[node_uri] = n
                    break

            if not node_exists:
                node = graph.addNode()
                uri_to_node[node_uri] = node
                for key, value in item.items():
                    prop = graph.getStringProperty(key)
                    prop[node] = str(value)
                    if key == "http://vital.ai/ontology/vital-core#hasName":
                        label_prop[node] = str(value)

        for item in result_list:
            source_uri = item.get('http://vital.ai/ontology/vital-core#hasEdgeSource')
            destination_uri = item.get('http://vital.ai/ontology/vital-core#hasEdgeDestination')

            if not source_uri or not destination_uri:
                continue

            source_node = uri_to_node.get(source_uri)
            destination_node = uri_to_node.get(destination_uri)

            if source_node and destination_node:
                edge = graph.addEdge(source_node, destination_node)
                for key, value in item.items():
                    # if key not in ['sourceURI', 'destinationURI']:
                    prop = graph.getStringProperty(key)
                    prop[edge] = str(value)

        for item in result_list:
            # third pass to create edges between
            # entities and slot nodes
            # for each slot, get entity uri
            # get node of entity uri
            # check if edge from entity to slot
            # if no, add it

            class_uri = item.get('type')

            if class_uri == 'http://vital.ai/ontology/haley-ai-kg#KGEntitySlot':
                uri = item.get('URI')
                entity_uri = item.get('http://vital.ai/ontology/haley-ai-kg#hasEntitySlotValue')

                if entity_uri:
                    node_a = uri_to_node.get(uri)
                    node_b = uri_to_node.get(entity_uri)
                    if node_a and node_b:
                        edge_list = self.find_edges_between_nodes(node_a, node_b)
                        if len(edge_list) == 0:
                            edge = graph.addEdge(node_a, node_b)

        return True

    def find_edges_between_nodes(self, node_a, node_b):

        graph = self.graph

        edges_between_nodes = []

        # Get all edges connected to node_a
        for edge in graph.getInOutEdges(node_a):
            # Check if the edge is connected to node_b
            source = graph.source(edge)
            target = graph.target(edge)
            if (source == node_a and target == node_b) or (source == node_b and target == node_a):
                edges_between_nodes.append(edge)

        return edges_between_nodes


tulipplugins.registerPluginOfGroup("KGraphNexusGraphExplore", "3. KGraphNexusGraphExplore", "Marc Hadfield", "13/07/2024", "KGraphNexusGraphExplore Info", "0.1.0", "KGraph Query")

