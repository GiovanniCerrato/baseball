import itertools

from database.DAO import DAO
import networkx as nx


class Model:
    def __init__(self):
        self._idMapTeams = {}
        self._graph = nx.Graph()
        self._squadre = None

    def buildGraph(self):
        self._graph.clear()
        self._addNodes()
        self._addEdges()

    def _addNodes(self):
        self._graph.add_nodes_from(self._squadre)
        return

    def _addEdges(self):
        myedges = list(itertools.combinations(self._squadre, 2))
        self._graph.add_edges_from(myedges)
        for e in self._graph.edges:
            salTot = 0
            sal1 = e[0].salarioTotale
            sal2 = e[1].salarioTotale
            salTot = sal1 + sal2
            self._graph[e[0]][e[1]]["weight"] = salTot
        return

    def getDettagliGrafo(self,squadra):
        vicini = self._graph.neighbors(squadra)
        listaDettagli = []
        for v in vicini:
            listaDettagli.append((v,self._graph[squadra][v]["weight"]))
        listaDettagli.sort(key = lambda x:x[0].salarioTotale, reverse = True)
        return listaDettagli



    def getAnni(self):
        return DAO.getAnni()

    def getSquadreAnno(self,anno):
        self._squadre = DAO.getSquadreAnno(anno)
        for s in self._squadre:
            self._idMapTeams[s.teamCode] = s
        return self._squadre

