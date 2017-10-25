import networkx
from src.BackDoor import BackDoorChecker

from src.TestDSeparation import makeSimpleGraph, makeMoreComplicatedGraph, makeIntermediateGraph
import matplotlib.pyplot as plt

__author__ = 'Spencer'

# Need to validate test cases!!
# Write down the Dagitty output for the intermediate graph below TODO

def main():
    plot = False
    g = makeIntermediateGraph()

    if plot:
        plt.figure(figsize=(20, 10))
        networkx.draw_networkx(g, with_labels=True, arrows=True)

    BackDoorChecker.listAdjustments()

    if plot:
        plt.show()