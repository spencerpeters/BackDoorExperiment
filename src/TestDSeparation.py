import matplotlib.pyplot as plt
import networkx

from ClientCodeForR.GraphConverter import GraphConverter
from src.DSeparation import DSeparator

__author__ = 'Spencer'


def main():
    plot = False

    if plot:
        g = makeSimpleGraph()
        # g = makeMoreComplicatedGraph()
        plt.figure(figsize=(20, 10))
        networkx.draw_networkx(g, with_labels=True, arrows=True)

    testSimpleGraph()
    print("\n")
    testMoreComplicatedGraph()

    if plot:
        plt.show()


def makeSimpleGraph():
    g = networkx.DiGraph()
    g.add_nodes_from([1, 2, 3])
    g.add_edges_from([(1, 2), (2, 3)])
    return g


def testSimpleGraph():
    g = makeSimpleGraph()
    d = DSeparator()
    Y = d.DSeparatedBy(g, [1], [2])

    print("Simple graph test.")
    print("The correct answer is: ")
    trueAnswer = sorted([3])
    print("Our answer is: ")
    print(sorted(Y))
    print("Are these two things the same?")
    print(sorted(Y) == trueAnswer)


def makeMoreComplicatedGraph():
    c = GraphConverter()

    # this graph was randomly generated in R using dagitty::randomDAG
    g = c.dagittyToNetworkX(
        "dag {\nx1\nx10\nx11\nx12\nx13\nx14\nx15\nx16\nx17\nx18\nx19\nx2\nx20\nx3\nx4\nx5\nx6\nx7\nx8\nx9\n"
        "x1 -> x12\nx1 -> x14\nx1 -> x17\nx1 -> x5\nx10 -> x18\nx10 -> x19\nx11 -> x12\nx11 -> x16\nx12 -> x15"
        "\nx12 -> x16\nx13 -> x15\nx13 -> x17\nx14 -> x19\nx15 -> x18\nx15 -> x19\nx15 -> x20\nx16 -> x17\nx16 -> x18"
        "\nx2 -> x17\nx2 -> x8\nx3 -> x11\nx3 -> x15\nx3 -> x17\nx3 -> x6\nx3 -> x9\nx4 -> x10\nx4 -> x14\nx4 -> x18"
        "\nx5 -> x20\nx6 -> x10\nx6 -> x13\nx6 -> x14\nx6 -> x15\nx6 -> x9\nx7 -> x11\nx7 -> x16\nx7 -> x8\nx8 -> x10"
        "\nx9 -> x18\n}\n")
    return g


def testMoreComplicatedGraph():
    g = makeMoreComplicatedGraph()
    d = DSeparator()
    Y = d.DSeparatedBy(g, ["x1", "x2"], ["x3", "x4"])

    print("More complicated graph test.")
    print("The correct answer is: ")
    trueAnswer = sorted(["x11", "x13", "x6", "x7", "x9"])
    print("Our answer is: ")
    print(sorted(Y))
    print("Are these two things the same?")
    print(sorted(Y) == trueAnswer)

    # to reproduce this result, import the dagitty library in R and run
    # testGraph = "dag {\nx1\nx10\nx11\nx12\nx13\nx14\nx15\nx16\nx17\nx18\nx19\nx2\nx20\nx3\nx4\nx5\nx6\nx7\nx8\nx9\n"
    #     "x1 -> x12\nx1 -> x14\nx1 -> x17\nx1 -> x5\nx10 -> x18\nx10 -> x19\nx11 -> x12\nx11 -> x16\nx12 -> x15"
    #     "\nx12 -> x16\nx13 -> x15\nx13 -> x17\nx14 -> x19\nx15 -> x18\nx15 -> x19\nx15 -> x20\nx16 -> x17\nx16 -> x18"
    #     "\nx2 -> x17\nx2 -> x8\nx3 -> x11\nx3 -> x15\nx3 -> x17\nx3 -> x6\nx3 -> x9\nx4 -> x10\nx4 -> x14\nx4 -> x18"
    #     "\nx5 -> x20\nx6 -> x10\nx6 -> x13\nx6 -> x14\nx6 -> x15\nx6 -> x9\nx7 -> x11\nx7 -> x16\nx7 -> x8\nx8 -> x10"
    #     "\nx9 -> x18\n}\n"
    # for (i in nodes) {if( dagitty::dseparated(testGraph, X = c("x1", "x2"), Y = c(i), Z = c("x3", "x4"))){print(i)}}
    # This will show a list of all nodes dseparated from x1 and x2 by x3 and x4;
    # the list will coincide with the trueAnswer above, EXCEPT that the dagitty answer
    # contains the nodes in Z, x3 and x4, which properly should not be considered as either dseparated or dconnected
    # from X by Z.


def makeIntermediateGraph():
    # this graph was randomly generated in R using dagitty::randomDAG
    g = GraphConverter.dagittyToNetworkX(
        "dag {\nx1\nx10\nx2\nx3\nx4\nx5\nx6\nx7\nx8\nx9\n"
        "x1 -> x10\nx2 -> x3\nx2 -> x7\nx2 -> x9\nx3 -> x5\n"
        "x3 -> x9\nx4 -> x9\nx5 -> x7\nx6 -> x10\nx6 -> x7\n"
        "x6 -> x8\nx7 -> x10\nx7 -> x9\nx9 -> x10\n}\n")
    return g

if __name__ == '__main__':
    main()
