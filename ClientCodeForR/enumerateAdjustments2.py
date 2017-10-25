__author__ = 'Spencer'
import sys

from oldCode.AdjustmentEnumerator import AdjustmentEnumerator


def main():
    if (len(sys.argv) != 7):
        print("Usage: python enumerateAdjustments.py rScriptFilename JSONFilename #graphs #nodes probabilityOfEdge outFilename")
        exit(1)

    rScriptFilepath = sys.argv[1]
    JSONFilepath = sys.argv[2]
    numGraphs = int(sys.argv[3])
    numNodes = int(sys.argv[4])
    connectionParameter = float(sys.argv[5])
    outputFilepath = sys.argv[6]
    outputFile = open(outputFilepath, 'w')

    enumerator = AdjustmentEnumerator(rScriptFilepath, JSONFilepath, outputFilepath)
    enumerator.getAdjustments(numGraphs, numNodes, connectionParameter)

if __name__ == '__main__':
    main()