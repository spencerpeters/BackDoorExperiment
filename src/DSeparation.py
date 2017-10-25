import random
import networkx
from collections import deque

LABEL = 'label'
DETERMINED = 'determined'
DESCENDANT = 'descendant'
START_NODE = "DSeparatorStartNode"
REACHABLE = 'reachable'
__author__ = 'Spencer'


class DSeparator:
    def __init__(self):
        pass

    @staticmethod
    def DSeparatedBy(graph: networkx.DiGraph, X, Z):
        DSeparator.verify(graph, [X, Z])

        # retains original topology and gets labels
        unmodifiedGraph = graph.copy()

        # gets new edges (D' in Pearl's Algorithm)
        # and edge BFS labels
        modifiedGraph = graph.copy()

        # step 1
        DSeparator.makeDescendants(unmodifiedGraph, Z)
        DSeparator.makeDetermined(unmodifiedGraph, Z)

        # step 2
        for edge in modifiedGraph.edges():
            modifiedGraph.add_edge(*edge, label=False)
            reverse = (edge[1], edge[0])
            modifiedGraph.add_edge(*reverse, label=False)

        # step 3 (Apply Pearl's Algorithm 1)

        modifiedGraph.add_node(START_NODE)
        queue = deque()

        # add dummy start edges and mark vertices X as reachable; initialize all others as unreachable
        for node in modifiedGraph.nodes():
            modifiedGraph.node[node][REACHABLE] = False

        modifiedGraph.node[START_NODE][REACHABLE] = True

        for alpha in X:
            modifiedGraph.node[alpha][REACHABLE] = True

            # add dummy edges
            edge = (START_NODE, alpha)
            reverse = (alpha, START_NODE)
            modifiedGraph.add_edge(*edge)
            modifiedGraph.add_edge(*reverse)
            queue.append(edge)
            DSeparator.updateEdgeLabel(modifiedGraph, edge, True)

        # find all paths.
        # Simple BFS over edges. Reachable edges.
        while not len(queue) == 0:
            # bfs stuff
            currentEdge = queue.popleft()
            u = currentEdge[0]
            v = currentEdge[1]

            # We know we can get to v; where can we go from v?

            # we can traverse the original out edges
            outList = unmodifiedGraph.out_edges(v)

            # or the new out edges created from the original in edges
            inList = [(e[1], e[0]) for e in unmodifiedGraph.in_edges(v)]

            edgesToConsider = []
            if u == START_NODE:
                edgesToConsider.extend(inList)
                edgesToConsider.extend(outList)
            else:
                UVForwardInOriginalGraph = unmodifiedGraph.has_edge(u, v)

                if UVForwardInOriginalGraph and unmodifiedGraph.node[v][DESCENDANT]:
                    edgesToConsider.extend(inList)
                elif UVForwardInOriginalGraph and not unmodifiedGraph.node[v][DESCENDANT]:
                    edgesToConsider.extend(outList)
                elif (not UVForwardInOriginalGraph) and (not unmodifiedGraph.node[v][DETERMINED]):
                    edgesToConsider.extend(outList)
                    edgesToConsider.extend(inList)

            for nextEdge in edgesToConsider:
                assert nextEdge[0] == v
                w = nextEdge[1]

                # check other conditions before adding nextEdge to the queue

                # unlabeled:
                if DSeparator.getEdgeLabel(modifiedGraph, nextEdge):
                    continue
                # loop:
                elif u == w:
                    continue
                else:
                    queue.append(nextEdge)
                    DSeparator.updateEdgeLabel(modifiedGraph, nextEdge, True)
                    modifiedGraph.node[w][REACHABLE] = True

        # this ends the BFS
        # perform the set differences and return
        modifiedGraph.remove_nodes_from(X)
        modifiedGraph.remove_nodes_from(Z)
        return [node for node in modifiedGraph.nodes() if not modifiedGraph.node[node][REACHABLE]]

    @staticmethod
    def verify(graph: networkx.DiGraph, setOfSetsOfNodes):
        assert (type(graph) == networkx.DiGraph)
        for nodeSet in setOfSetsOfNodes:
            for node in nodeSet:
                assert (graph.has_node(node))

    @staticmethod
    def verifyEdges(graph, E):
        for edge in E:
            assert graph.has_edge(edge)

    @staticmethod
    def updateEdgeLabel(graph, edge, newLabel):
        graph.add_edge(edge[0], edge[1], label=newLabel)

    @staticmethod
    def getEdgeLabel(graph, edge):
        return graph.edge[edge[0]][edge[1]][LABEL]

    @staticmethod
    def makeDescendants(graph: networkx.DiGraph, Z):
        # initialize everything to False
        for node in graph.nodes():
            graph.add_node(node, descendant=False)

        # walk backwards from children to parents marking true, starting with
        # nodes in Z
        queue = deque()
        for node in Z:
            queue.append(node)
        while not len(queue) == 0:
            currentNode = queue.popleft()
            graph.add_node(currentNode, descendant=True)
            parents = graph.predecessors(currentNode)
            for parent in parents:
                if not graph.node[parent][DESCENDANT]:
                    queue.append(parent)

    @staticmethod
    def makeDetermined(graph, Z):
        # initialize everything to False
        for node in graph.nodes():
            graph.node[node][DETERMINED] = False

        # initialize nodes to True
        for node in Z:
            graph.node[node][DETERMINED] = True

    @staticmethod
    def randomDAG(n, p, seed=None):
        random.seed(seed)
        g = networkx.DiGraph()
        g.add_nodes_from(range(0, n))

        for i in range(0, n):
            for j in range(i + 1, n):
                if (random.random() < p):
                    g.add_edge(i, j)

        return g
