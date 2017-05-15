__author__ = 'Spencer'
import sys
import subprocess
import json
import numpy as np
from src.AdjustmentEnumerator import AdjustmentEnumerator

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

    enumerator = AdjustmentEnumerator(rScriptFilepath, JSONFilepath, outputFilepath)
    enumerator.getAdjustments(numGraphs, numNodes, connectionParameter)

if __name__ == '__main__':
    main()