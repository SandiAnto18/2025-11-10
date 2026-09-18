
import networkx as nx
from database.DAO import DAO


class Model:

    def __init__(self):
        self._graph = nx.DiGraph()  # GRAFO ORIENTATO altrimenti nx.Graph()

    def getStores(self):
        return DAO.getAllStores()
    def buildGraph(self,store_name,k):

        # SVUOTO IL GRAFO PRECEDENTE
        self._graph.clear()

        # RECUPERO GLI ORDINI DELLO STORE SELEZIONATO
        orders = DAO.getAllOrders(store_name)

        # AGGIUNGO GLI ORDINI COME NODI DEL GRAFO
        self._graph.add_nodes_from(orders)

        arco = DAO.getOrder1Order2(store_name,k)

        self._graph.add_edges_from(arco)

        peso= /k

    def getNodes(self):
        return len(self._graph.nodes())

    def getEdges(self):
        return len(self._graph.edges())

    def getTop5(self):
        edges = sorted(self._graph.edges(data=True), key=lambda x: x[2]['weight'], reverse=True)
        return edges[:5]
