__author__ = 'Spencer'

import networkx as nx

def main():
    G = nx.Graph()
    G.add_nodes_from([1, 2])
    G.add_edge(1, 2)
    print(G.neighbors(1))

if __name__ == '__main__':
    main()