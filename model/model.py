
import networkx as nx
from database.DAO import DAO


class Model:

    def __init__(self):
        self._graph = nx.DiGraph()  # GRAFO ORIENTATO altrimenti nx.Graph()

    def getStores(self):
        return DAO.getAllStores()
    def buildGraph(self,store_name):

        # SVUOTO IL GRAFO PRECEDENTE
        self._graph.clear()

        # RECUPERO GLI ORDINI DELLO STORE SELEZIONATO
        orders = DAO.getAllOrders(store_name)

        # AGGIUNGO GLI ORDINI COME NODI DEL GRAFO
        self._graph.add_nodes_from(orders)

    def getNodes(self):
        return len(self._graph.nodes())

    def getEdges(self):
        return len(self._graph.edges())
