import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._graph=nx.DiGraph()
        self._idMap= {}
    def getStores(self):
        return DAO.getStores()

    def getOrders(self,store_name):
        return DAO.getOrders(store_name)

    def buildGraph(self,store_name,k):
        orders = DAO.getOrders(store_name)
        # SVUOTO IL GRAFO PRECEDENTE
        self._graph.clear()

        # AGGIUNGO I PILOTI COME NODI
        self._graph.add_nodes_from(orders)

        self._idMap = {}
        for d in orders:
            self._idMap[d.order_id] = d

        # RECUPERO LE COPPIE DI PILOTI E I PESI
        archi = DAO.getArchi(store_name,k)

        # AGGIUNGO GLI ARCHI CON IL LORO PESO
        for g1, g2, peso in archi:
            gene1 = self._idMap[g1]
            gene2 = self._idMap[g2]


            self._graph.add_edge(
                gene1,
                gene2,
                weight=peso
            )
        print(archi)

    def getNumNodi(self):
        # RESTITUISCO IL NUMERO DI NODI
        return self._graph.number_of_nodes()

    def getNumArchi(self):
        # RESTITUISCO IL NUMERO DI ARCHI
        return self._graph.number_of_edges()

    def getTop5(self):
        edges = sorted(self._graph.edges(data=True), key=lambda x: x[2]['weight'], reverse=True)
        return edges[:5]
    # output (order1,order2,{"weight": peso})

    def getCamminoPiuLungo(self, sourceStr):

        # RECUPERO IL NODO DI PARTENZA TRAMITE IL SUO ORDER_ID
        source = self._idMap[int(sourceStr)]

        # CREO L'ALBERO DFS PARTENDO DAL NODO SELEZIONATO
        tree = nx.dfs_tree(self._graph, source)

        # INIZIALIZZO IL CAMMINO PIU' LUNGO
        lp = []

        # SCORRO TUTTI I NODI RAGGIUNGIBILI NELL'ALBERO DFS
        for node in tree.nodes:

            # RECUPERO IL PERCORSO DAL NODO INIZIALE AL NODO CORRENTE
            tmp = nx.shortest_path(tree, source, node)

            # CONTROLLO SE IL PERCORSO TROVATO E' PIU' LUNGO
            if len(tmp) > len(lp):
                lp = tmp

        # RESTITUISCO IL CAMMINO PIU' LUNGO
        return lp

