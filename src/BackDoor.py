import itertools

import networkx

from ClientCodeForR.GraphConverter import GraphConverter
from src.DSeparation import DSeparator

__author__ = 'Spencer'


def test():
    g = GraphConverter.dagittyToNetworkX("dag {\nx1\nx10\nx2\nx3\nx4\nx5\nx6\nx7\nx8\nx9\n"
                                         "x1 -> x10\nx1 -> x5\nx1 -> x8\nx1 -> x9\nx3 -> x10\n"
                                         "x3 -> x5\nx3 -> x7\nx3 -> x8\nx4 -> x10\nx4 -> x5\n"
                                         "x4 -> x7\nx5 -> x6\nx5 -> x8\nx5 -> x9\nx6 -> x7\n"
                                         "x6 -> x9\nx8 -> x10\n}\n")

    adj = BackDoorChecker.listMinimalAdjustments(g, ["x9"], ["x4"])
    print(adj)

    allAdj = BackDoorChecker.listAllAdjustmentsForAllTreatments(g, ["x4"])
    print(allAdj)


# Need to make more test cases
# and update existing test cases so that they match what we put into Dagitty's Adjustment Sets

class BackDoorChecker:
    @staticmethod
    def satisfiesBackDoor(graph: networkx.DiGraph, X, Z, Y):

        # remove all edges from nodes in X to nodes not in X
        # then check whether Y is a subset of DSeparatedBY(graph, X, Z)
        # Can enumerate all adjustment sets by going through all possible Z for given X (gross)
        # Try and profile.
        # guess I don't really need this :P
        graph = BackDoorChecker.backDoorGraph(graph)

        return BackDoorChecker.satisfiesBackDoorOnBackDoorGraph(graph, X, Z, Y)

    @staticmethod
    def backDoorGraph(graph, X):
        graph = graph.copy()

        xSet = set(X)

        for x in X:
            outEdges = graph.out_edges(x)
            for edge in outEdges:
                v = edge[1]
                if v in xSet:
                    graph.remove_edge(x, v)

        return graph

    @staticmethod
    def satisfiesBackDoorOnBackDoorGraph(backDoorGraph: networkx.DiGraph, X, Z, Y):
        d = DSeparator()
        Ymax = d.DSeparatedBy(backDoorGraph, X, Z)
        Y = set(Y)
        Ymax = set(Ymax)
        if Ymax.issuperset(Y):
            return True
        return False

    @staticmethod
    # return a dictionary, where the keys are treatment sets
    # and the values are lists of (all, minimal) sets of nodes representing valid adjustments for that treatment.
    def listAllAdjustmentsForAllTreatments(graph: networkx.DiGraph, Y, isMinimal=True):
        Xmax = set(graph.nodes()).difference(Y)
        powerSet = [set(X) for X in BackDoorChecker.powerset(Xmax)]

        result = dict()
        for X in powerSet:
            result[frozenset(X)] = BackDoorChecker.listAdjustments(graph, X, Y, isMinimal)

        return result

    @staticmethod
    # return a list of sets (all, minimal) of nodes representing valid adjustments
    def listAdjustments(graph: networkx.DiGraph, X, Y, isMinimal=True):
        if isMinimal:
            return BackDoorChecker.listMinimalAdjustments(graph, X, Y)
        else:
            return BackDoorChecker.listAllAdjustments(graph, X, Y)

    # return a list of all sets of nodes representing valid adjustments
    @staticmethod
    def listAllAdjustments(graph: networkx.DiGraph, X, Y):
        Zmax = set(graph.nodes()).difference(X).difference(Y)
        powerSet = [set(z) for z in BackDoorChecker.powerset(Zmax)]  # list of all subsets of Zmax as sets

        backDoorGraph = BackDoorChecker.backDoorGraph(graph, X)

        result = []

        while len(powerSet) > 0:
            Z = powerSet.pop()
            if BackDoorChecker.satisfiesBackDoorOnBackDoorGraph(backDoorGraph, X, Z, Y):
                result.append(Z)

        return result

    # return a list of subset-minimal sets of nodes representing valid adjustments
    @staticmethod
    def listMinimalAdjustments(graph: networkx.DiGraph, X, Y):
        Zmax = set(graph.nodes()).difference(X).difference(Y)
        powerSet = [set(z) for z in BackDoorChecker.powerset(Zmax)]  # list of all subsets of Zmax as sets

        backDoorGraph = BackDoorChecker.backDoorGraph(graph, X)

        result = []

        setIsMinimal = [True] * len(powerSet)
        isAdjustment = [False] * len(powerSet)

        powerSet.sort(key=lambda elem: len(elem))  # shortest elements eliminate more supersets

        for i in range(len(powerSet)):
            if setIsMinimal[i]:
                Z = powerSet[i]
                if BackDoorChecker.satisfiesBackDoorOnBackDoorGraph(backDoorGraph, X, Z, Y):
                    isAdjustment[i] = True

                    # This loop is inefficient (rethink)
                    for j in range(i + 1, len(powerSet)):
                        if powerSet[j].issuperset(Z):
                            setIsMinimal[j] = False

        for i in range(len(powerSet)):
            if setIsMinimal[i] and isAdjustment[i]:
                result.append(powerSet[i])

        return result

    @staticmethod
    def powerset(iterable):
        "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
        s = list(iterable)
        return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s) + 1))


if __name__ == '__main__':
    test()
