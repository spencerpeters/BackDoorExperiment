import networkx

__author__ = 'Spencer'


class TakataSeparator:

    # From Takata, Space-optimal, backtracking algorithms to list the minimal vertex separators of a graph,
    # Discrete Applied Mathematics, 2010, page 1663
    @staticmethod
    def closeSeparator(graph: networkx.Graph, vertexSetA, b):
        neighborhoodOfA = networkx.node_boundary(graph, vertexSetA)

        # can this be optimized away?
        graph = graph.copy()
        graph.remove_nodes_from(neighborhoodOfA)

        verticesOfConnectedComponentContainingB = networkx.node_connected_component(graph, b)

        return set(networkx.node_boundary(graph, verticesOfConnectedComponentContainingB))

    # From Takata, Space-optimal, backtracking algorithms to list the minimal vertex separators of a graph,
    # Discrete Applied Mathematics, 2010, page 1664
    # A: nodes that must be contained in a's connected component after separation by any returned separator
    # U: nodes that must not be contained in a's connected component
    @staticmethod
    def listMinimalSeparators(graph: networkx.Graph, a, b):
        results = set()
        return TakataSeparator.listMinimalSeparatorsPrivate(graph, [a], graph.neighbors(b), a, b, results)

    @staticmethod
    def listMinimalSeparatorsPrivate(graph: networkx.Graph, A, U, a, b, results):
        # given A, compute componentOfSeparatedGraphContainingA, which is V(Ca(S(A)))
        SeparatorA = TakataSeparator.closeSeparator(graph, A, b)
        separatedGraph = graph.copy()
        separatedGraph.remove_nodes_from(SeparatorA)
        componentOfSeparatedGraphContainingA = networkx.node_connected_component(separatedGraph, a)
        if len(componentOfSeparatedGraphContainingA.union(U)) == 0:  # subtree is not barren
            newA = componentOfSeparatedGraphContainingA
            neighborhoodOfNewA = set(networkx.node_boundary(newA))
            possibleExpansions = set(neighborhoodOfNewA).difference(U)
            if len(possibleExpansions) != 0:
                for v in possibleExpansions:
                    TakataSeparator.listMinimalSeparatorsPrivate(graph, newA.union(v), U, a, b, results)
                    TakataSeparator.listMinimalSeparatorsPrivate(graph, newA, U.union(v), a, b, results)
            else:  # base case, node is a leaf
                results.add(TakataSeparator.closeSeparator(newA))
        else:
            # The subtree is barren.
            pass
