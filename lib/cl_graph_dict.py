# class Cl_graph
# Node is a dataclass with an unique ID n_id assigned internally by the class, and a string s_label
# Link is a number
# internally stores the g_d_graph as dictionary, where the key is a tuple of two strings
# g_d_node : set
# g_d_link : dict
#
# methods:
# add_node( i_s_name)
# add_link_one_way( i_s_node_start, i_s_node_end, i_n_link_weight )
# add_link_two_way( i_s_node_start, i_s_node_end, i_n_link_weight )
# get_weight( i_s_start, i_s_end )
# get_neighbour( i_s_node : str ) -> list
# iter_node that iterate g_d_nodes
# iter_neighbour(i_s_node) that iterates neigbour of a node
# show that use twoo iterators to show the
#
# make a test with four fully connected cities, link are distances, and make an exploration using iterators

from dataclasses import dataclass

@dataclass
class Node:
    n_id: int
    s_label: str


class Cl_graph:
    def __init__(self):
        self.g_d_node = {}   # label -> Node
        self.g_d_link = {}   # (start_label, end_label) -> weight
        self._next_id = 0

    # -------- nodes --------
    def add_node(self, i_s_name: str):
        if i_s_name not in self.g_d_node:
            self.g_d_node[i_s_name] = Node(self._next_id, i_s_name)
            self._next_id += 1

    # -------- links --------
    def add_link_one_way(self, i_s_node_start, i_s_node_end, i_n_link_weight):
        self.add_node(i_s_node_start)
        self.add_node(i_s_node_end)
        self.g_d_link[(i_s_node_start, i_s_node_end)] = i_n_link_weight

    def add_link_two_way(self, i_s_node_start, i_s_node_end, i_n_link_weight):
        self.add_link_one_way(i_s_node_start, i_s_node_end, i_n_link_weight)
        self.add_link_one_way(i_s_node_end, i_s_node_start, i_n_link_weight)



    # -------- query --------

    @property
    def num_node(self) -> int:
        return len(self.g_d_node)

    def get_node(self):
        return self.g_d_node.keys()

    def get_node_index( self, i_s_node_name : str ) -> int:
        return self.g_d_node[i_s_node_name].n_id

    def get_weight(self, i_s_start, i_s_end):
        return self.g_d_link.get((i_s_start, i_s_end))

    def get_neighbour(self, i_s_node):
        ls_neighbour = list()
        for (start, end), weight in self.g_d_link.items():
            if start == i_s_node:
                ls_neighbour.append((end, weight))
        return ls_neighbour

    # -------- iterators for link as node indices --------
    def iter_link_node_index(self):
        """
        Iterate over links but return node indices instead of labels.
        Example: ('Rome','Paris',800) -> (0,2,800)
        """
        for (start_label, end_label), w in self.g_d_link.items():
            start_id = self.g_d_node[start_label].n_id
            end_id = self.g_d_node[end_label].n_id
            yield start_id, end_id, float(w)

    # -------- iterators --------
    def iter_node(self):
        for node in self.g_d_node.values():
            yield node

    def iter_neighbour(self, i_s_node):
        for (start, end), w in self.g_d_link.items():
            if start == i_s_node:
                yield end, w

    # -------- display --------
    def show(self):
        print("Nodes:")
        for n in self.iter_node():
            print(f"  {n.n_id}: {n.s_label}")

        print("\nLinks:")
        for (a, b), w in self.g_d_link.items():
            print(f"  {a} -> {b} = {w}")


# ---------------- TEST ----------------
if __name__ == "__main__":
    g = Cl_graph()

    cities = ["Milan", "Rome", "Paris", "Berlin"]

    # fully connected graph (distances are fictional)
    distances = {
        ("Milan", "Rome"): 480,
        ("Rome", "Paris"): 850,
        ("Paris", "Berlin"): 1000,
        ("Berlin", "Zurich"): 2000,
    }

    for (a, b), d in distances.items():
        g.add_link_two_way(a, b, d)

    print( f"Nodes: {g.get_node()}" )

    g.show()

    print("\nExploration using iterators:\n")

    # iterate nodes
    for node in g.iter_node():
        print(f"From {node.s_label}:")
        for neigh, w in g.iter_neighbour(node.s_label):
            print(f"   -> {neigh} ({w} km)")
        print()