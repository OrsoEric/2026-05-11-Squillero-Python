# create a class graph with some operation
# Cl_graph
# it has a numpy matrix to store weights
# nodes have a string name
# method add_node( i_s_name)
# method add_link_one_way( i_s_node_start, i_s_node_end, i_n_link_weight )
# method add_link_two_way( i_s_node_start, i_s_node_end, i_n_link_weight )
# method show that will list the nodes, the links

"""
.venv\Scripts\activate

python excercise_6_graph.py

------------------------------------------

print(f"\nNeighbours of {s_target} (ITERATOR):")

for s_neighbour in cl_graph.neighbour_iter(s_target):
    print(f" - {s_neighbour}")
    
Neighbours of London (ITERATOR):
 - Paris
 - Amsterdam
 
-------------------------------------------

lls_adjacent = cl_graph.show_adjacent()

for s_node, l_links in zip(cl_graph.l_s_nodes, lls_adjacent):
    print(f"\n{s_node} ->")
    for s_neigh, n_w in l_links:
        print(f"   {s_neigh} ({n_w} km)")


Paris ->
   London (344.0 km)
   Berlin (878.0 km)
   Rome (1105.0 km)
   Madrid (1053.0 km)

London ->
   Paris (344.0 km)
   Amsterdam (357.0 km)

Berlin ->
   Paris (878.0 km)
   Rome (1184.0 km)
   Amsterdam (577.0 km)

Rome ->
   Paris (1105.0 km)
   Berlin (1184.0 km)
   Madrid (1365.0 km)

Madrid ->
   Paris (1053.0 km)
   Rome (1365.0 km)

Amsterdam ->
   London (357.0 km)
   Berlin (577.0 km)

---------------------------

print(f"\nITERATE ADJACENCY")
for s_node in cl_graph.iter_node():
    print(f"\nNeighbours of {s_node}:")
    for s_neighbour in cl_graph.neighbour_iter(s_node):
        print(f">{s_neighbour} - {cl_graph.get_link_weight(s_node,s_neighbour)}")

ITERATE ADJACENCY

Neighbours of Paris:
>London - 344.0
>Berlin - 878.0
>Rome - 1105.0
>Madrid - 1053.0

Neighbours of London:
>Paris - 344.0
>Amsterdam - 357.0

Neighbours of Berlin:
>Paris - 878.0
>Rome - 1184.0
>Amsterdam - 577.0

Neighbours of Rome:
>Paris - 1105.0
>Berlin - 1184.0
>Madrid - 1365.0

Neighbours of Madrid:
>Paris - 1053.0
>Rome - 1365.0

Neighbours of Amsterdam:
>London - 357.0
>Berlin - 577.0

"""
import numpy as np
from typing import Optional

from typing import Iterator


class Cl_graph:
    def __init__(self) -> None:
        self.l_s_nodes: list[str] = []
        self.np_matrix: np.ndarray = np.zeros((0, 0), dtype=float)

    # ---------------------------------------------------------
    # Add a node
    # ---------------------------------------------------------
    def add_node(self, i_s_name: str) -> bool:

        # Check input type
        if not isinstance(i_s_name, str):
            print("ERROR: node name must be a string")
            return False

        # Check empty string
        if i_s_name.strip() == "":
            print("ERROR: node name cannot be empty")
            return False

        # Check duplicates
        if i_s_name in self.l_s_nodes:
            print(f"ERROR: node '{i_s_name}' already exists")
            return False

        self.l_s_nodes.append(i_s_name)

        n_size: int = len(self.l_s_nodes)

        # Resize adjacency matrix
        np_new_matrix: np.ndarray = np.zeros(
            (n_size, n_size),
            dtype=float
        )

        if self.np_matrix.size > 0:
            np_new_matrix[:-1, :-1] = self.np_matrix

        self.np_matrix = np_new_matrix

        return True

    # ---------------------------------------------------------
    # Internal helper
    # ---------------------------------------------------------
    def _get_node_index(self, i_s_name: str) -> Optional[int]:

        if not isinstance(i_s_name, str):
            print("ERROR: node name must be a string")
            return None

        if i_s_name not in self.l_s_nodes:
            print(f"ERROR: node '{i_s_name}' does not exist")
            return None

        return self.l_s_nodes.index(i_s_name)

    # ---------------------------------------------------------
    # Add one-way link
    # ---------------------------------------------------------
    def add_link_one_way(
        self,
        i_s_node_start: str,
        i_s_node_end: str,
        i_n_link_weight: float
    ) -> bool:

        # Check weight type
        if not isinstance(i_n_link_weight, (int, float)):
            print("ERROR: link weight must be numeric")
            return False

        n_start: Optional[int] = self._get_node_index(
            i_s_node_start
        )

        n_end: Optional[int] = self._get_node_index(
            i_s_node_end
        )

        if n_start is None or n_end is None:
            return False

        self.np_matrix[n_start, n_end] = float(
            i_n_link_weight
        )

        return True

    # ---------------------------------------------------------
    # Add two-way link
    # ---------------------------------------------------------
    def add_link_two_way(
        self,
        i_s_node_start: str,
        i_s_node_end: str,
        i_n_link_weight: float
    ) -> bool:

        # Check weight type
        if not isinstance(i_n_link_weight, (int, float)):
            print("ERROR: link weight must be numeric")
            return False

        n_start: Optional[int] = self._get_node_index(
            i_s_node_start
        )

        n_end: Optional[int] = self._get_node_index(
            i_s_node_end
        )

        if n_start is None or n_end is None:
            return False

        self.np_matrix[n_start, n_end] = float(
            i_n_link_weight
        )

        self.np_matrix[n_end, n_start] = float(
            i_n_link_weight
        )

        return True

    
    # ---------------------------------------------------------
    # Get link weight
    # ---------------------------------------------------------
    def get_link_weight(
        self,
        i_s_node_start: str,
        i_s_node_end: str
    ) -> Optional[float]:

        # Validate inputs
        if not isinstance(i_s_node_start, str) or not isinstance(i_s_node_end, str):
            print("ERROR: node names must be strings")
            return None

        n_start = self._get_node_index(i_s_node_start)
        n_end = self._get_node_index(i_s_node_end)

        if n_start is None or n_end is None:
            return None

        weight = self.np_matrix[n_start, n_end]

        # Treat 0 as "no link"
        if weight == 0:
            return None

        return float(weight)

    # ---------------------------------------------------------
    # Get neighbours
    # ---------------------------------------------------------
    def get_neighbour(
        self,
        i_s_node: str
    ) -> list[str]:

        l_s_neighbours: list[str] = []

        # Check input type
        if not isinstance(i_s_node, str):
            print("ERROR: node name must be a string")
            return l_s_neighbours

        n_node_index: Optional[int] = self._get_node_index(
            i_s_node
        )

        if n_node_index is None:
            return l_s_neighbours

        # Scan adjacency matrix row
        for n_col, n_weight in enumerate(
            self.np_matrix[n_node_index]
        ):

            if n_weight != 0:
                l_s_neighbours.append(
                    self.l_s_nodes[n_col]
                )

        return l_s_neighbours

    # ---------------------------------------------------------
    # Node iterator
    # ---------------------------------------------------------
    def iter_node(self) -> Iterator[str]:
        """
        Iterate over all node names in the graph.
        """

        for s_node in self.l_s_nodes:
            yield s_node

    # ---------------------------------------------------------
    # Neighbour iterator
    # ---------------------------------------------------------

    def neighbour_iter(
        self,
        i_s_node: str
    ) -> Iterator[str]:

        # Check input type
        if not isinstance(i_s_node, str):
            print("ERROR: node name must be a string")
            return

        n_node_index: Optional[int] = self._get_node_index(
            i_s_node
        )

        if n_node_index is None:
            return

        # Iterate through adjacency matrix row
        for n_col, n_weight in enumerate(
            self.np_matrix[n_node_index]
        ):

            if n_weight != 0:
                yield self.l_s_nodes[n_col]

    def show_adjacent(
        self
    ) -> list[list[tuple[str, float]]]:

        l_result: list[list[tuple[str, float]]] = []

        # For each node (row in adjacency matrix)
        for n_row, s_node in enumerate(self.l_s_nodes):

            l_connections: list[tuple[str, float]] = []

            # Scan all possible connections
            for n_col, n_weight in enumerate(self.np_matrix[n_row]):

                if n_weight != 0:
                    l_connections.append(
                        (self.l_s_nodes[n_col], float(n_weight))
                    )

            l_result.append(l_connections)

        return l_result

    # ---------------------------------------------------------
    # Show graph
    # ---------------------------------------------------------
    def show(self) -> bool:

        print("===================================")
        print("EUROPEAN CAPITALS")
        print("===================================")

        for n_index, s_node in enumerate(self.l_s_nodes):
            print(f"{n_index} -> {s_node}")

        print("\n===================================")
        print("DISTANCES")
        print("===================================")

        for n_row, s_start in enumerate(self.l_s_nodes):

            for n_col, s_end in enumerate(self.l_s_nodes):

                n_weight: float = self.np_matrix[
                    n_row,
                    n_col
                ]

                if n_weight != 0:
                    print(
                        f"{s_start} -> {s_end} "
                        f"= {n_weight:.0f} km"
                    )

        lls_adjacent = self.show_adjacent()

        for s_node, l_links in zip(cl_graph.l_s_nodes, lls_adjacent):
            print(f"\n{s_node} ->")
            for s_neigh, n_w in l_links:
                print(f"   {s_neigh} ({n_w} km)")


        print("\n===================================")
        print("ADJACENCY MATRIX")
        print("===================================")

        print(self.np_matrix)

        return True


# =============================================================
# TEST BENCH
# =============================================================
if __name__ == "__main__":

    cl_graph: Cl_graph = Cl_graph()

    # ---------------------------------------------------------
    # Add European capitals
    # ---------------------------------------------------------
    cl_graph.add_node("Paris")
    cl_graph.add_node("London")
    cl_graph.add_node("Berlin")
    cl_graph.add_node("Rome")
    cl_graph.add_node("Madrid")
    cl_graph.add_node("Amsterdam")

    # ---------------------------------------------------------
    # Add distances (km)
    # Approximate road/air distances
    # ---------------------------------------------------------

    cl_graph.add_link_two_way(
        "Paris",
        "London",
        344
    )

    cl_graph.add_link_two_way(
        "Paris",
        "Berlin",
        878
    )

    cl_graph.add_link_two_way(
        "Paris",
        "Madrid",
        1053
    )

    cl_graph.add_link_two_way(
        "Paris",
        "Rome",
        1105
    )

    cl_graph.add_link_two_way(
        "London",
        "Amsterdam",
        357
    )

    cl_graph.add_link_two_way(
        "Amsterdam",
        "Berlin",
        577
    )

    cl_graph.add_link_two_way(
        "Berlin",
        "Rome",
        1184
    )

    cl_graph.add_link_two_way(
        "Madrid",
        "Rome",
        1365
    )

    # ---------------------------------------------------------
    # Invalid tests
    # ---------------------------------------------------------
    cl_graph.add_node("Paris")

    cl_graph.add_link_one_way(
        "Paris",
        "Lisbon",
        500
    )

    cl_graph.add_link_one_way(
        "Paris",
        "Rome",
        "BAD_WEIGHT"  # type: ignore
    )

    # ---------------------------------------------------------
    # Show graph
    # ---------------------------------------------------------
    cl_graph.show()
    
    s_target = "London"
    s_target_neighbour = cl_graph.get_neighbour(s_target)
    print(f"neighbour to {s_target} are {s_target_neighbour} ")

    # ---------------------------------------------------------
    # Iterate nodes
    # ---------------------------------------------------------

    print("\nAll nodes in graph: (ITERATOR)")

    for s_node in cl_graph.iter_node():
        print(f" - {s_node}")

    # ---------------------------------------------------------
    # Iterate neighbours
    # ---------------------------------------------------------
    print(f"\nNeighbours of {s_target} (ITERATOR):")

    for s_neighbour in cl_graph.neighbour_iter(s_target):
        print(f" - {s_neighbour}")

    # ---------------------------------------------------------
    # ADJACENCY LIST
    # ---------------------------------------------------------

    lls_adjacent = cl_graph.show_adjacent()

    for s_node, l_links in zip(cl_graph.l_s_nodes, lls_adjacent):
        print(f"\n{s_node} ->")
        for s_neigh, n_w in l_links:
            print(f"   {s_neigh} ({n_w} km)")


    # ---------------------------------------------------------
    # ITERATE ADJACENCY
    # ---------------------------------------------------------

    print(f"\nITERATE ADJACENCY")
    for s_node in cl_graph.iter_node():
        print(f"\nNeighbours of {s_node}:")
        for s_neighbour in cl_graph.neighbour_iter(s_node):
            print(f">{s_neighbour} - {cl_graph.get_link_weight(s_node,s_neighbour)}")