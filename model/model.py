import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._idMapA = {}

    def buildGraph(self, genre):
        self._graph.clear()

        self._artists = DAO.getAllNodes(genre)
        for a in self._artists:
            self._idMapA[a.ArtistId] = a
        self._graph.add_nodes_from(self._artists)

        edges = DAO.getAllEdges(genre, self._idMapA)
        for e in edges:
            self._graph.add_edge(e.a1, e.a2, weight = e.peso)

    def getArtists(self):
        return self._graph.nodes()

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getTop5Archi(self):  # 3 archi di peso maggiore
        return sorted(self._graph.edges(data=True), key=lambda x: x[2]["weight"], reverse=True)[:5]

    def getBestInfluenzaArtista(self):
        #MIGLIOR INFLUENZA PESO ARC USCETE - PESO ARC ENTRANTE
        listNodesPesata = []
        for n in self._graph.nodes:
            score = 0
            for a in self._graph.out_edges(n, data=True):  # arco uscente  #data = true : dammi gli attributi
                score += a[2]["weight"]  # il peso perchè è una tupla
            for a in self._graph.in_edges(n, data=True):  # entranti
                score -= a[2]["weight"]
            listNodesPesata.append((n, score))

        listNodesPesata.sort(key=lambda x: x[1], reverse=True)
        return listNodesPesata[0]

    def getAllGenre(self):
        return DAO.getAllGenre()

