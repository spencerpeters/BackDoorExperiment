__author__ = 'Spencer'
import sys
import subprocess
import json
import numpy as np
import math

def main():
    if (len(sys.argv) != 7):
        print("Usage: python enumerateAdjustments.py rScriptFilepath JSONFilepath #graphs #nodes probabilityOfEdge outFilepath")
        exit(1)

    rScriptFilepath = sys.argv[1]
    JSONFilepath = sys.argv[2]
    numGraphs = int(sys.argv[3])
    numNodes = int(sys.argv[4])
    connectionParameter = float(sys.argv[5])
    outputFilepath = sys.argv[6]
    outputFile = open(outputFilepath, 'w')

    subprocess.call(["Rscript",
                     rScriptFilepath,
                     str(numGraphs),
                     str(numNodes),
                     str(connectionParameter),
                     JSONFilepath])

    result = json.load(open(JSONFilepath))

    sizes = []
    powerSetSize = 2**(numNodes - 1)
    for i in range(len(result)):
        graphData = result[i]
        graphSizes = []
        sizes.append(graphSizes)
        outputFile.write("===Graph " + str(i) + "===\n\n")
        for j in range(len(graphData)):
            sinkData = graphData[j]
            sinkNode = sinkData[0]
            cuboidAndAdjustments = sinkData[1]
            reformattedCuboidAndAdjustments = reformatR(cuboidAndAdjustments, True)
            currentSize = len(reformattedCuboidAndAdjustments)
            graphSizes.append(currentSize)
            outputFile.write("Effect Variable " + str(sinkNode[0]))
            outputFile.write("\n")
            outputFile.write(str(currentSize))
            outputFile.write("\n")
            outputFile.write(str(reformattedCuboidAndAdjustments))
            outputFile.write("\n\n")

    print("PARAMETERS: Nodes Per Graph " + str(numNodes), "Connection Parameter " + str(connectionParameter))
    print("Total number of possible cuboids (power set size): " + str(powerSetSize))
    averages = [np.mean(graphSizes) for graphSizes in sizes]
    print("Average number of useful cuboids by graph, to nearest integer:" + str([round(avg) for avg in averages]))
    print("Average number of useful cuboids over all graphs: " + str(np.mean(averages)))
    outputFile.close()

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

if __name__ == '__main__':
    main()
