import networkx
from src.DSeparation import DSeparator

LABEL = 'label'
DETERMINED = 'determined'
DESCENDANT = 'descendant'
START_NODE = "DSeparatorStartNode"
REACHABLE = 'reachable'

__author__ = 'Spencer'


class TakataDSeparator:


    # Note! This is for D-separation. So D-separation in the back-door graph gives
    @staticmethod
    def moralGraph(graph: networkx.DiGraph, X, Y, Z):
        moralGraph = graph.copy()
        DSeparator.makeDescendants(moralGraph, X.union(Y).union(Z))
        for node in moralGraph.nodes():
            if not node[DESCENDANT]:  # if the node is not an ancestor of any of the nodes in X, Y, Z
                moralGraph.remove_node(node)
            node[DESCENDANT] = False  # clear DESCENDANT markers

            DSeparator.makeDescendants(moralGraph, Z)

        # not sure if this strategy for moralizing the graph is efficient (I can imagine examples where it is very bad)
        # eg, all nodes in set P have edges to all children in set C

        # go find an algorithm for moralizing a graph (Koller??)
        for node in moralGraph.nodes():
            if node[DESCENDANT]:  # if the node is an ancestor of a node in Z, or if it is in Z
                parents = list(node.parents())
                for i in range(len(parents)):
                    for j in range(i + 1, len(parents)):
                        graph.add_edge(parents[i], parents[j])

        return graph.to_undirected(graph)