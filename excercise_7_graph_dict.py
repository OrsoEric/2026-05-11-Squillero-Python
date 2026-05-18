# class cl_graph
# internally stores the graph as dictionary, where the key is a tuple of two strings
# methods:
# add_node( i_s_name)
# add_link_one_way( i_s_node_start, i_s_node_end, i_n_link_weight )
# add_link_two_way( i_s_node_start, i_s_node_end, i_n_link_weight )
# add get_weight( i_s_start, i_s_end )
# add iter_node that iterate nodes
# add iter_neighbour(i_s_node) that iterates neigbour of a node
# add show that use twoo iterators to show the
#
# TEST BENCH
# add a __main__ example
# it's the distance of rail connectionss between five european cities

class Cl_graph:
    def __init__(self):
        # (start, end) -> weight
        self.graph = {}
        self.nodes = set()

    # -------------------------
    # Core operations
    # -------------------------
    def add_node(self, i_s_name):
        self.nodes.add(i_s_name)

    def add_link_one_way(self, i_s_node_start, i_s_node_end, i_n_link_weight):
        self.add_node(i_s_node_start)
        self.add_node(i_s_node_end)
        self.graph[(i_s_node_start, i_s_node_end)] = i_n_link_weight

    def add_link_two_way(self, i_s_node_start, i_s_node_end, i_n_link_weight):
        self.add_link_one_way(i_s_node_start, i_s_node_end, i_n_link_weight)
        self.add_link_one_way(i_s_node_end, i_s_node_start, i_n_link_weight)

    # -------------------------
    # New required methods
    # -------------------------
    def get_weight(self, i_s_start, i_s_end):
        """Return weight of edge or None if not exists."""
        return self.graph.get((i_s_start, i_s_end))

    def iter_nodes(self):
        """Iterator over nodes."""
        return iter(self.nodes)

    def iter_neighbours(self, i_s_node):
        """Iterator over neighbours of a node."""
        for (start, end), weight in self.graph.items():
            if start == i_s_node:
                yield end, weight

    # -------------------------
    # Display using iterators
    # -------------------------
    def show(self):
        """Display graph using iterators."""
        print("GRAPH STRUCTURE")
        print("================")

        for node in self.iter_nodes():
            print(f"\n{node} ->")

            found = False
            for neighbour, weight in self.iter_neighbours(node):
                print(f"   > {neighbour} ({weight} km)")
                found = True

            if not found:
                print("   (no connections)")




# -------------------------
# TEST BENCH
# -------------------------

def test_bench():
    cl_graph = Cl_graph()

    # Five European cities
    cities = ["London", "Paris", "Brussels", "Amsterdam", "Berlin"]

    # Add nodes explicitly (optional since links also add them)
    for c in cities:
        cl_graph.add_node(c)

    # Rail distances (approximate, km)
    cl_graph.add_link_two_way("London", "Paris", 450)
    cl_graph.add_link_two_way("London", "Brussels", 320)
    cl_graph.add_link_two_way("Paris", "Brussels", 300)
    cl_graph.add_link_two_way("Brussels", "Amsterdam", 200)
    cl_graph.add_link_two_way("Amsterdam", "Berlin", 650)
    cl_graph.add_link_two_way("Paris", "Berlin", 1050)

    print("Rail network graph (edges):")
    cl_graph.show()

if __name__ == "__main__":
    test_bench()