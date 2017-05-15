__author__ = 'Spencer'

import sys
import subprocess
import json
import numpy as np

class AdjustmentEnumerator:

    def __init__(self, rScriptFilepath, JSONFilepath, outputFilepath):
        self.rScriptFilepath = rScriptFilepath
        self.JSONFilepath = JSONFilepath
        self.outputFilepath = outputFilepath
        self.outputFile = open(outputFilepath)

        self.sizes = None
        self.reformattedCuboidsAndAdjustmentsList = None

    def getAdjustments(self, numGraphs, numNodes, connectionParameter, toFile=True, summarize=True):
        rawResult = self.callRScript(self.rScriptFilepath, numGraphs, numNodes, connectionParameter, self.JSONFilepath)
        finalResult = self.parseResults(rawResult, numNodes, toFile)
        self.printResults(finalResult, numGraphs, numNodes, connectionParameter)

    def printResults(self, results, numGraphs, numNodes, connectionParameter):
        print("PARAMETERS: Nodes Per Graph " + str(numNodes), "Connection Parameter " + str(connectionParameter))
        print("Total number of possible cuboids (power set size): " + str(2**(numNodes -1)))
        averages = [np.mean(graphSizes) for graphSizes in sizes]
        print("Average number of useful cuboids by graph:" + str(averages))
        print("Average number of useful cuboids over all graphs: " + str(np.mean(averages)))

    def parseResults(self, result, numNodes, toFile):
        sizes = []
        reformattedCuboidsAndAdjustmentsList = []
        powerSetSize = 2**(numNodes - 1)
        for i in range(len(result)):
            graphData = result[i]
            graphSizes = []
            sizes.append(graphSizes)
            if toFile:
                self.outputFile.write("===Graph " + str(i) + "===\n\n")
            for j in range(len(graphData)):
                sinkData = graphData[j]
                sinkNode = sinkData[0]
                cuboidAndAdjustments = sinkData[1]
                reformattedCuboidAndAdjustments = reformatR(cuboidAndAdjustments, True)
                reformattedCuboidsAndAdjustmentsList.append(reformattedCuboidAndAdjustments)
                currentSize = len(reformattedCuboidAndAdjustments)
                graphSizes.append(currentSize)
                if toFile:
                    self.outputFile.write("Effect Variable " + str(sinkNode[0]))
                    self.outputFile.write("\n")
                    self.outputFile.write(str(currentSize))
                    self.outputFile.write("\n")
                    self.outputFile.write(str(reformattedCuboidAndAdjustments))
                    self.outputFile.write("\n\n")

        return {"sizes": sizes, reformattedCuboidAndAdjustments)

    def callRScript(self, rScriptFilepath, numGraphs, numNodes, connectionParameter, JSONFilepath):
        subprocess.call(["Rscript",
                     rScriptFilepath,
                     str(numGraphs),
                     str(numNodes),
                     str(connectionParameter),
                     JSONFilepath])

        result = json.load(open(JSONFilepath))
        return result


def reformatR(x, pretty=False):
    y = []
    for ta in x:
        treatment = ta[0]
        adjustments = ta[1]
        adjustmentsList = adjustments.values()
        y.append([treatment, adjustmentsList])

    # we want to map closures to lists of admissible treatments. The number of unique closures is what is relevant.
    z = {}
    for ta in y:
        treatment = ta[0]
        adjustments = ta[1]
        for adj in adjustments:
            closureList = (treatment + adj)
            if [] in closureList:
                closureList.remove([])
            closureList.sort()
            closure = tuple(closureList)
            if closure not in z:
                z[closure] = [adj]
            else:
                z[closure].append(adj)

        if (pretty):
            for closure in z.keys():
                z[closure] = prettify(z[closure])
    return z

def prettify(adjustments):
    if adjustments == []:
        return ["no admissible adjustments"]
    else:
        return [explain(adj) for adj in adjustments]


def explain(adj):
    if adj == []:
        return ["empty adjustment"]
    else:
        return adj