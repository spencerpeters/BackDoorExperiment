__author__ = 'Spencer'
import networkx as nx


def test():
    c = GraphConverter()
    originalDagitty = "dag {\nx1\nx10\nx2\nx3\nx4\nx5\nx6\nx7\nx8\nx9\n" \
        "x1 -> x10\nx2 -> x3\nx2 -> x7\nx2 -> x9\nx3 -> x5\n" \
        "x3 -> x9\nx4 -> x9\nx5 -> x7\nx6 -> x10\nx6 -> x7\n" \
        "x6 -> x8\nx7 -> x10\nx7 -> x9\nx9 -> x10\n}\n"
    print("The original graph is \n" + originalDagitty)
    nxGraph = c.dagittyToNetworkX(originalDagitty)

    # originalDagitty = "dag {\na\nb\na -> b\n}\n"
    # nxGraph = c.dagittyToNetworkX(originalDagitty)

    print("The edges and nodes of the resulting networkX graph are:")
    print(nxGraph.edges())
    print(nxGraph.nodes())
    print("\n")

    revertedDagitty = c.networkXToDagitty(nxGraph)

    print("The graph below is the original graph, converted back and forth from networkX form.")
    print("The two graphs are the same, up to a reordering of variables and edges.")
    print(revertedDagitty)


class GraphConverter:

    def __init__(self):
        pass

    # This method only works on dagitty dag graph strings in the format
    # in which they are displayed:
    # "dag {\n<node1>\n<node2>\n...\n<nodeN>\n<edge1>\n<edge2>\n<edgeN>\n}\n"
    # where <nodei> is an arbitrary string (without a newline)
    # and <edgei> is of the form "<nodej> -> <nodek>".
    # an example is "dag {\na\nb\na -> b\n}\n"
    # Note that DAGs can be parsed by dagitty::dagitty in more general syntax, so be careful.
    # The function will likely fail an assertion and quit if its format assumptions are violated, but I can't guarantee.
    @staticmethod
    def dagittyToNetworkX(dagittyGraphString):
        nxGraph = nx.DiGraph()

        graphType = dagittyGraphString[0:3]
        assert graphType == "dag"
        openBrace = dagittyGraphString[3:5]
        assert openBrace == " {"
        closeBrace = dagittyGraphString[-3:len(dagittyGraphString)]
        assert closeBrace == "\n}\n"
        content = dagittyGraphString[5:-3]
        tokens = content.split()
        assert(len(tokens) > 1)
        currentIndex = 0
        currentToken = tokens[currentIndex]
        nextToken = tokens[currentIndex + 1]
        while (nextToken != "->"):
            nxGraph.add_node(currentToken)
            currentIndex += 1

            if (currentIndex + 1 >= len(tokens)):
                break

            currentToken = tokens[currentIndex]
            nextToken = tokens[currentIndex + 1]

        if (currentIndex + 1 < len(tokens)):  # we've hit an arrow
            fro = currentToken
            to = tokens[currentIndex + 1 + 1]
            nxGraph.add_edge(fro, to)
            currentIndex = currentIndex + 3

            while (currentIndex < len(tokens)):
                fro = tokens[currentIndex]
                to = tokens[currentIndex + 2]
                nxGraph.add_edge(fro, to)

                currentIndex = currentIndex + 3

        return nxGraph

    @staticmethod
    def networkXToDagitty(graph: nx.DiGraph):
        dagittyGraphString = "dag {"

        for node in graph.nodes():
            dagittyGraphString = dagittyGraphString + "\n" + node

        for edge in graph.edges():
            dagittyGraphString = dagittyGraphString + "\n" + edge[0] + " -> " + edge[1]

        dagittyGraphString += "\n}\n"
        return dagittyGraphString


if __name__ == '__main__':
    test()