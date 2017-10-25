import networkx
from src.BackDoor import BackDoorChecker
from collections import defaultdict
from src.TestDSeparation import makeIntermediateGraph
import json
import pickle

adjustmentFilepath = "/Users/Spencer/PycharmProjects/BackDoorExperiment/adjustmentForIntermediateGraph.json"

__author__ = 'Spencer'

# TODO need to test converter

def test():
    # graph = makeIntermediateGraph()
    # sink = AdjustmentEnumeratorPython.findSinks(graph)[0]

    # TODO figure out why no adjustments are being returned
    # it looks like this is failing (returning no adjustments). What is going on? Is it the graph,
    # or problem with BackDoor? Need to test BackDoor more thoroughly and examine the graph.
    # TODO make a graph plotting routine
    # TODO organize methods.
    # adjustments = BackDoorChecker.listAllAdjustmentsForAllTreatments(graph, sink)
    # adjustmentFile = open(adjustmentFilepath, "wb")
    # pickle.dump(adjustments, adjustmentFile)
    # adjustmentFile.close()
    adjustmentFile = open(adjustmentFilepath, "rb")
    adjustments = pickle.load(adjustmentFile)
    print(adjustments)

    closures = AdjustmentEnumeratorPython.convertTreatmentToAdjustmentDictToClosureToTreatmentDict(adjustments)
    print(closures)


class AdjustmentEnumeratorPython:

    # Returns a dictionary mapping sinks to
    # dictionaries mapping treatment sets to lists of sets representing valid adjustments
    @staticmethod
    def EnumerateAdjustments(graph: networkx.DiGraph, minimal=True):
        sinks = AdjustmentEnumeratorPython.findSinks(graph)

        result = dict()
        for sink in sinks:
            adjustmentForCurrentSink = BackDoorChecker.listAllAdjustmentsForAllTreatments(graph, sink, minimal)

            result[sink] = frozenset(adjustmentForCurrentSink)

        return result

    # input is a dictionary mapping treatment sets to lists of sets representing valid adjustments
    # as returned by BackDoor.listAllAdjustmentsForAllTreatments.
    # returns a dictionary mapping sets of nodes having at least one valid partition into treatment and adjustment,
    # into all the subsets t that correspond to valid treatment = t, adjustment = V - t
    @staticmethod
    def convertTreatmentToAdjustmentDictToClosureToTreatmentDict(treatmentToAdjustmentDict: dict):
        result = defaultdict(set)
        for treatment in treatmentToAdjustmentDict.keys():
            adjustmentList = treatmentToAdjustmentDict[treatment]
            for adjustment in adjustmentList:
                closure = treatment.union(adjustment)
                result[closure].add(treatment)

        return result

    @staticmethod
    def findSinks(graph: networkx.DiGraph):
        return [node for node in graph.nodes() if graph.out_degree(node) == 0]

if __name__ == '__main__':
    test()


