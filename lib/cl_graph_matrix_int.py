# class Cl_graph
# Node is an integer
# internally stores the g_lln_weight as numpy matrix
#
# methods:
# add_node( i_n_node)
# add_link_one_way( i_n_node_start, i_n_node_end, i_n_link_weight )
# add_link_two_way( i_n_node_start, i_n_node_end, i_n_link_weight )
# get_weight( i_n_node_id : int )
# get_node() -> list of node_id
# get_neighbour( i_n_node : int ) -> list
# iter_node that iterate nodes
# iter_neighbour(i_n_node) that iterates neigbour of a node
# show that use twoo iterators to show the
#
# make a test with a linear graph with 5 cities and their distance and explore the graph navigating neighbouring nodes with a queue usingneighbour iterator

import numpy as np
from collections import deque


class Cl_graph:
    """
    Graph class using:
    - integer node IDs
    - adjacency matrix stored as numpy array
    """

    def __init__(self):
        self.l_node = []
        self.d_node_index = {}
        self.g_lln_weight = np.zeros((0, 0), dtype=float)

    # -------------------------------------------------
    # NODE MANAGEMENT
    # -------------------------------------------------

    def add_node(self, i_n_node):
        if i_n_node in self.d_node_index:
            return

        self.l_node.append(i_n_node)
        self.d_node_index[i_n_node] = len(self.l_node) - 1

        n_size = len(self.l_node)

        # resize adjacency matrix
        g_new = np.zeros((n_size, n_size), dtype=float)

        if n_size > 1:
            g_new[:-1, :-1] = self.g_lln_weight

        self.g_lln_weight = g_new

    # -------------------------------------------------
    # LINK MANAGEMENT
    # -------------------------------------------------

    def add_link_one_way(
        self,
        i_n_node_start,
        i_n_node_end,
        i_n_link_weight
    ):
        n_row = self.d_node_index[i_n_node_start]
        n_col = self.d_node_index[i_n_node_end]

        self.g_lln_weight[n_row, n_col] = i_n_link_weight

    def add_link_two_way(
        self,
        i_n_node_start,
        i_n_node_end,
        i_n_link_weight
    ):
        self.add_link_one_way(
            i_n_node_start,
            i_n_node_end,
            i_n_link_weight
        )

        self.add_link_one_way(
            i_n_node_end,
            i_n_node_start,
            i_n_link_weight
        )

    # -------------------------------------------------
    # ACCESS METHODS
    # -------------------------------------------------

    def get_weight(self, i_n_node_id):
        n_index = self.d_node_index[i_n_node_id]
        return self.g_lln_weight[n_index]

    def get_node(self):
        return list(self.l_node)

    def get_neighbour(self, i_n_node):
        n_row = self.d_node_index[i_n_node]

        l_neighbour = list()

        for n_col, n_weight in enumerate(self.g_lln_weight[n_row]):
            if n_weight != 0:
                l_neighbour.append(self.l_node[n_col])

        return l_neighbour

    # -------------------------------------------------
    # ITERATORS
    # -------------------------------------------------

    def iter_node(self):
        for n_node in self.l_node:
            yield n_node

    def iter_neighbour(self, i_n_node):
        n_row = self.d_node_index[i_n_node]

        for n_col, n_weight in enumerate(self.g_lln_weight[n_row]):
            if n_weight != 0:
                yield self.l_node[n_col]

    # -------------------------------------------------
    # SHOW GRAPH
    # -------------------------------------------------

    def show(self):
        print("GRAPH")

        for n_node in self.iter_node():

            print(f"\nNode {n_node}")

            for n_neighbour in self.iter_neighbour(n_node):
                n_weight = self.get_weight( n_neighbour )
                print(f"  -> {n_neighbour}  weight={n_weight}")


# =====================================================
# TEST
# Linear graph with 5 cities
# =====================================================

if __name__ == "__main__":

    g = Cl_graph()

    # cities
    CITY_MILAN = 1
    CITY_PARMA = 2
    CITY_BOLOGNA = 3
    CITY_FLORENCE = 4
    CITY_ROME = 5

    # add nodes
    for n_city in [
        CITY_MILAN,
        CITY_PARMA,
        CITY_BOLOGNA,
        CITY_FLORENCE,
        CITY_ROME
    ]:
        g.add_node(n_city)

    # linear connections
    g.add_link_two_way(CITY_MILAN,    CITY_PARMA,    125)
    g.add_link_two_way(CITY_PARMA,    CITY_BOLOGNA,  100)
    g.add_link_two_way(CITY_BOLOGNA,  CITY_FLORENCE, 105)
    g.add_link_two_way(CITY_FLORENCE, CITY_ROME,     275)

    # show graph
    g.show()

    # =================================================
    # BFS navigation using neighbour iterator
    # =================================================

    print("\n")
    print("BFS EXPLORATION")

    q_node = deque()

    n_start = CITY_MILAN

    q_node.append(n_start)

    s_visited = set()
    s_visited.add(n_start)

    while len(q_node) > 0:

        n_current = q_node.popleft()

        print(f"\nCurrent node: {n_current}")

        for n_neighbour, n_weight in g.iter_neighbour(n_current):

            print(
                f"  neighbour={n_neighbour}"
                f" distance={n_weight}"
            )

            if n_neighbour not in s_visited:
                s_visited.add(n_neighbour)
                q_node.append(n_neighbour)