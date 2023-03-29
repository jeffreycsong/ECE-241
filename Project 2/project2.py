import random
import csv
import pythonds as ds
import sys


class ISPNetwork:

    def __init__(self):
        self.network = Graph()
        self.MST = Graph()

    def buildGraph(self, filename):
        file = list(csv.reader(open(filename, 'r')))
        for i in file:
            self.network.addEdge(i[0], i[1], float(i[2]))
            self.network.addEdge(i[1], i[0], float(i[2]))

    def reset(self):
        for v in self.network:
            v.dist = sys.maxsize
            v.pred = None
            v.color = 'white'
        for v in self.MST:
            v.dist = sys.maxsize
            v.pred = None
            v.color = 'white'

    def resetMST(self):
        for v in self.MST:
            v.dist = sys.maxsize
            v.pred = None
            v.color = 'white'


    def pathExist(self, router1, router2):
        self.reset()
        rv1 = self.network.getVertex(router1)
        isPath = self.bfs(rv1,router2)

        return isPath

    def bfs(self, start, end):
        vertQueue = ds.Queue()
        vertQueue.enqueue(start)
        while (vertQueue.size() > 0):
            currentVert = vertQueue.dequeue()
            if currentVert is not None:
                for nbr in currentVert.getConnections():
                    if (nbr.getColor() == 'white'):
                        if nbr.getId() == end:
                            return True
                        nbr.setColor('gray')
                        vertQueue.enqueue(nbr)
                    currentVert.setColor('black')
        return False

    def buildMST(self):


        lister = list(self.network.getVertices())

        self.prim(self.network, self.network.getVertex(lister[0]))
        for v in self.network:
            for connections in v.getConnections():
                if connections.getPred() == v:
                    self.MST.addEdge(connections.getId(), v.getId(), v.getWeight(connections))
                    self.MST.addEdge(v.getId(), connections.getId(), v.getWeight(connections))



    def prim(self, G, start):
        pq = ds.PriorityQueue()
        for v in G:
            v.setDistance(sys.maxsize)
            v.setPred(None)
        start.setDistance(0)
        pq.buildHeap([(v.getDistance(), v) for v in G])
        while not pq.isEmpty():
            currentVert = pq.delMin()
            for nextVert in currentVert.getConnections():
                newCost = currentVert.getWeight(nextVert)
                if nextVert in pq and newCost < nextVert.getDistance():
                    nextVert.setPred(currentVert)
                    nextVert.setDistance(newCost)
                    pq.decreaseKey(nextVert, newCost)

    def findPath(self, router1, router2):
        pathlist = []
        spath = ''
        r1vm = self.MST.getVertex(router1)
        r2vm = self.MST.getVertex(router2)
        if r1vm is not None:
            self.dijkstra(self.MST, r1vm)
        while r2vm is not None and r2vm.getColor() == 'white':
            if r2vm == r1vm:
                break
            r2vm.setColor('black')
            pathlist.append(r2vm.getId())
            r2vm = r2vm.getPred()
        if r2vm is not None:
            pathlist.append(r2vm.getId())
        if router1 in pathlist:
            pathlist.reverse()
            for i in pathlist:
                if i == router2:
                    spath = spath + i
                else:
                    spath = spath + i + ' -> '
        else:
            spath = 'path not exist'


        self.resetMST()
        return spath

    def dijkstra(self, aGraph, start):
        pq = ds.PriorityQueue()
        start.setDistance(0)
        pq.buildHeap([(v.getDistance(), v) for v in aGraph])
        while not pq.isEmpty():
            currentVert = pq.delMin()
            for nextVert in currentVert.getConnections():
                newDist = currentVert.getDistance() + currentVert.getWeight(nextVert)
                if newDist < nextVert.getDistance():
                    nextVert.setDistance(newDist)
                    nextVert.setPred(currentVert)
                    pq.decreaseKey(nextVert, newDist)

    def findForwardingPath(self, router1, router2):

        pathlist = []
        spath = ''
        weight = 0



        """
        pathlist = []
        spath = ''
        weight = 0
        r1v = self.network.getVertex(router1)
        r2v = self.network.getVertex(router2)

        if r1v is not None and self.network is not None:
            self.dijkstra(self.network, r1v)
            neighbors = r1v.getConnections()
        while r2v is not None and r2v.getColor() == 'white' and r2v.getPred() is not None:
            if r2v == r1v:
                break
            r2v.setColor('black')
            pathlist.append(r2v.getId())
            weight += r2v.getWeight(r2v.getPred())
            r2v = r2v.getPred()

            if r2v is not None:
                pathlist.append(r2v.getId())
            if router1 in pathlist:
                pathlist.reverse()
                for i in pathlist:
                    if i == router2:
                        spath = spath + i + '(' + str(weight) + ')'
                    else:
                        spath = spath + i + ' -> '
            else:
                spath = 'path not exist'

            self.reset()
            return spath
        """

    def findPathMaxWeight(self, router1, router2):
        pass

    @staticmethod
    def nodeEdgeWeight(v):
        return sum([w for w in v.connectedTo.values()])

    @staticmethod
    def totalEdgeWeight(g):
        return sum([ISPNetwork.nodeEdgeWeight(v) for v in g]) // 2

class Vertex:
    def __init__(self, key):
        self.id = key
        self.connectedTo = {}
        self.color = 'white'
        self.dist = sys.maxsize
        self.pred = None
        self.disc = 0
        self.fin = 0
        self.pathweight = 0

    def addNeighbor(self, nbr, weight=0):
        self.connectedTo[nbr] = weight

    def setColor(self, color):
        self.color = color

    def setDistance(self, d):
        self.dist = d

    def setPred(self, p):
        self.pred = p

    def setDiscovery(self, dtime):
        self.disc = dtime

    def setFinish(self, ftime):
        self.fin = ftime

    def getFinish(self):
        return self.fin

    def getDiscovery(self):
        return self.disc

    def getPred(self):
        return self.pred

    def getDistance(self):
        return self.dist

    def getColor(self):
        return self.color

    def getConnections(self):
        return self.connectedTo.keys()

    def getWeight(self, nbr):
        return self.connectedTo[nbr]

    def __str__(self):
        return str(self.id) + ' connectedTo: ' + str([x.id for x in self.connectedTo])

    def getId(self):
        return self.id

class Graph:
    def __init__(self):
        self.vertList = {}
        self.numVertices = 0

    def addVertex(self,key):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key)
        self.vertList[key] = newVertex
        return newVertex

    def getVertex(self,n):
        if n in self.vertList:
            return self.vertList[n]
        else:
            return None

    def __contains__(self,n):
        return n in self.vertList

    def addEdge(self,f,t,cost=0):
        if f not in self.vertList:
            nv = self.addVertex(f)
        if t not in self.vertList:
            nv = self.addVertex(t)
        self.vertList[f].addNeighbor(self.vertList[t], cost)

    def getVertices(self):
        return self.vertList.keys()

    def __iter__(self):
        return iter(self.vertList.values())



if __name__ == '__main__':
    print("--------- Task1 build graph ---------")
    # Note: You should try all six dataset. This is just a example using 1221.csv
    net = ISPNetwork()
    net.buildGraph('dataset/1221.csv')

    print("--------- Task2 check if path exists ---------")
    routers = [v.id for v in random.sample(list(net.network.vertList.values()), 5)]
    for i in range(4):
        print('Router1:', routers[i], ', Router2:', routers[i+1], 'path exist?:', net.pathExist(routers[i], routers[i+1]))

    print("--------- Task3 build MST ---------")
    net.buildMST()
    print('graph node size', net.MST.numVertices)
    print('graph total edge weights', net.totalEdgeWeight(net.MST))

    print("--------- Task4 find shortest path in MST ---------")
    for i in range(4):
        print(routers[i], routers[i+1], 'Path:', net.findPath(routers[i], routers[i+1]))

    print("--------- Task5 find shortest path in original graph ---------")
    for i in range(4):
        print(routers[i], routers[i+1], 'Path:', net.findForwardingPath(routers[i], routers[i+1]))

    print("--------- Task6 find path in LowestMaxWeightFirst algorithm ---------")
    for i in range(4):
        print(routers[i], routers[i+1], 'Path:', net.findPathMaxWeight(routers[i], routers[i+1]))
