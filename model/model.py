import itertools

import copy
from random import random

from database.DAO import DAO
import networkx as nx


class Model:
    def __init__(self):
        self._idMapTeams = {}
        self._graph = nx.Graph()
        self._squadre = None
        self._bestPath = []
        self._bestObjVal = 0

    def getPath(self,v0):
        self._bestPath = []
        self._bestObjVal = 0

        parziale = [v0]

        for v in self._graph.neighbors(v0):
            parziale.append(v)
            self._ricorsione(parziale)
            parziale.pop()

    def getPathV2(self, v0):
        self._bestPath = []
        self._bestObjVal = 0

        parziale = [v0]

        for v in self._graph.neighbors(v0):
            parziale.append(v)
            self._ricorsioneV2(parziale)
            parziale.pop()
        return self._bestPath, self._bestObjVal

    def _ricorsione(self, parziale):
        print(len(parziale))
        #1 condizione di ottimalità, verifico se la parziale è migliore del best
        if self._score(parziale) > self._bestObjVal:
            self._bestPath = copy.deepcopy(parziale)
            self._bestObjVal = self._score(parziale)

        #2 condizione di terminazione, verifico se posso continuare


        #3 faccio la ricorsione
        for v in self._graph.neighbors(parziale[-1]):
            pesoE = self._graph[parziale[-1]][v]["weight"]
            if self._graph[parziale[-2]][parziale[-1]]["weight"] > pesoE and v not in parziale:
                parziale.append(v)
                self._ricorsione(parziale)
                parziale.pop()

    def _ricorsioneV2(self, parziale):
        print(parziale)
        # 1 condizione di ottimalità, verifico se la parziale è migliore del best
        if self._score(parziale) > self._bestObjVal:
            self._bestPath = copy.deepcopy(parziale)
            self._bestObjVal = self._score(parziale)

        # 2 condizione di terminazione, verifico se posso continuare

        # 3 faccio la mia ricorsione
        # listaVicini = []
        # for v in self._grafo.neighbors(parziale[-1]):
        #     edgeV = self._grafo[parziale[-1]][v]["weight"]
        #     listaVicini.append((v, edgeV))
        #
        # listaVicini.sort(key= lambda x: x[1], reverse=True)

        listaVicini = self.getDettagliGrafo(parziale[-1])

        for v in listaVicini:
            if v[0] not in parziale and self._graph[parziale[-2]][parziale[-1]]["weight"] > v[1]:
                parziale.append(v[0])
                self._ricorsioneV2(parziale)
                parziale.pop()
                return





    def _score(self,parziale):
        score = 0
        for i in range(0,len(parziale)-1):
            score += self._graph[parziale[i]][parziale[i+1]]["weight"]
        return score

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

    def getRandomNode(self):
        return self._idMapTeams['LAN']

    def svuotaGrafo(self):
        self._graph.clear()
        return print("Grafo svuotato!")

    def esisteGrafo(self):
        if len(self._graph.nodes) == 0:
            return False
        return True

