from math import sqrt
from itertools import combinations
import re
from collections import deque

from pathlib import Path

#from graph_alist import cl_graph

#from excercise_7_graph_dict import Cl_graph

#from lib.cl_graph import Cl_graph

from lib.cl_graph_matrix_int import Cl_graph

C_S_FILE = Path( "data", "HCP", "alb1000.hcp" )
print("Looking for:", C_S_FILE.resolve())

def extract_field(marker: str, full_text: str) -> str:
    match = re.search(rf'{marker}\s*:(.*?)$', full_text, re.IGNORECASE | re.MULTILINE)
    if match:
        return match.group(1).strip().upper()
    else:
        return ""


def extract_section(marker: str, full_text: str) -> str:
    match = re.search(rf'{marker}(.*?)[-A-Z]', full_text, re.IGNORECASE | re.DOTALL)
    assert match, f"D'ho!? Can't find \"{marker.upper()}\"..."
    return match.group(1)


def read_graph(filename):
    # Open and read the entire HCP/TSP file as a single string
    with open(filename) as data:
        whole_file = data.read()

    # Extract metadata fields from the header
    name = extract_field('NAME', whole_file)
    comment = extract_field('COMMENT', whole_file)
    format = extract_field('EDGE_WEIGHT_TYPE', whole_file)

    # Some files use EDGE_DATA_FORMAT instead of EDGE_WEIGHT_TYPE
    if not format:
        format = extract_field('EDGE_DATA_FORMAT', whole_file)

    # Print basic dataset info
    print(name)
    print(comment)

    # Number of nodes (cities) in the graph
    n_cities = int(extract_field('DIMENSION', whole_file))

    # Create an empty graph structure
    cl_graph = Cl_graph()

    # -----------------------------
    # Case 1: Explicit distance matrix
    # -----------------------------
    if format == 'EXPLICIT':
        # Read all edge weights into a l_queue for sequential processing
        data = deque(
            int(d) for d in extract_section('EDGE_WEIGHT_SECTION', whole_file).split()
        )

        # Lower triangular matrix including diagonal
        if extract_field('EDGE_WEIGHT_FORMAT', whole_file) == 'LOWER_DIAG_ROW':
            for c1 in range(n_cities):
                for c2 in range(c1):
                    w = data.popleft()
                    cl_graph.add_node(c1)
                    cl_graph.add_node(c2)
                    cl_graph.add_link_one_way(c1, c2, w)
                    cl_graph.add_link_one_way(c2, c1, w)
                # diagonal element (self-loop) must be 0
                assert data.popleft() == 0

        # Upper triangular matrix format
        elif extract_field('EDGE_WEIGHT_FORMAT', whole_file) == 'UPPER_ROW':
            for c1 in range(n_cities):
                for c2 in range(1, n_cities - c1):
                    w = data.popleft()
                    cl_graph.add_node(c1)
                    cl_graph.add_node(c2)
                    cl_graph.add_link_one_way(c1, c2, w)
                    cl_graph.add_link_one_way(c2, c1, w)

    # -----------------------------
    # Case 2: Geometric coordinates (Euclidean distances)
    # -----------------------------
    elif format == 'ATT':
        cities = []

        # Parse node coordinates
        for l in extract_section('NODE_COORD_SECTION', whole_file).split('\n'):
            if not l.strip():
                continue
            _, x, y = map(int, l.split())
            cities.append((x, y))

        # Compute full pairwise distance matrix
        for c1, c2 in combinations(range(n_cities), r=2):
            d = sqrt(
                (cities[c1][0] - cities[c2][0]) ** 2 +
                (cities[c1][1] - cities[c2][1]) ** 2
            )
            cl_graph.add_node(c1)
            cl_graph.add_node(c2)
            cl_graph.add_link_one_way(c1, c2, d)
            cl_graph.add_link_one_way(c2, c1, d)

    # -----------------------------
    # Case 3: Explicit edge list
    # -----------------------------
    elif format == 'EDGE_LIST':
        for l in extract_section('EDGE_DATA_SECTION', whole_file).split('\n'):
            if not l.strip():
                continue

            n1, n2 = map(int, l.split())

            # Convert 1-based indexing to 0-based indexing
            cl_graph.add_node(n1-1)
            cl_graph.add_node(n2-1)
            #print(f"adding nodes {n1} and {n2}")
            cl_graph.add_link_one_way(n1 - 1, n2 - 1, 1)
            cl_graph.add_link_one_way(n2 - 1, n1 - 1, 1)

    # -----------------------------
    # Unsupported format
    # -----------------------------
    else:
        assert False, "Can't parse cl_graph!"

    # Return fully constructed graph object
    return cl_graph


def explore( i_cl_graph: Cl_graph, i_s_node_start: str ) -> bool:
    ds_visited = set()
    l_queue = deque()  # Start from node 0
    l_queue.append(i_s_node_start)

    while l_queue:
        s_node = l_queue.popleft()
        if s_node not in ds_visited:
            print(f"scanning: {s_node}")
            ds_visited.add(s_node)
            # Add neighbors to the l_queue

            ls_neighbor = i_cl_graph.get_neighbour(s_node)
            print(f"Node {s_node} has {len(ls_neighbor)} neighbours:{ls_neighbor}")

            for s_neighbor in i_cl_graph.iter_neighbour(s_node):
                print(f"Node {s_node} has Neighbour:{s_neighbor}")
                if s_neighbor not in ds_visited:
                    print(f"New node discovered: {s_neighbor}")
                    l_queue.append(s_neighbor)  



    return False #OK    

import heapq


def shortest_path(i_cl_graph: Cl_graph, start_node, end_node):
    """
    Compute the minimum-cost path between two nodes
    using Dijkstra's algorithm.

    Returns:
        (distance, path)
    """

    # Priority queue: (distance, node)
    pq = [(0, start_node)]

    # Distance from start to each node
    distances = {start_node: 0}

    # Previous node in optimal path
    previous = {}

    # Visited nodes
    visited = set()

    while pq:
        current_distance, current_node = heapq.heappop(pq)

        # Skip already processed nodes
        if current_node in visited:
            continue

        visited.add(current_node)

        # Stop if destination reached
        if current_node == end_node:
            break

        # Explore neighbours
        for neighbour in i_cl_graph.iter_neighbour(current_node):

            # Get edge weight
            weight = i_cl_graph.get_weight(current_node, neighbour)

            new_distance = current_distance + weight

            # Relaxation step
            if neighbour not in distances or new_distance < distances[neighbour]:
                distances[neighbour] = new_distance
                previous[neighbour] = current_node

                heapq.heappush(
                    pq,
                    (new_distance, neighbour)
                )

    # No path found
    if end_node not in distances:
        return float("inf"), []

    # Reconstruct path
    path = []
    node = end_node

    while node != start_node:
        path.append(node)
        node = previous[node]

    path.append(start_node)
    path.reverse()

    return distances[end_node], path

def test_bench():
    print(f"file: {C_S_FILE}")
    cl_graph = read_graph(C_S_FILE)

    l_nodes = list(cl_graph.get_node())
    d_start = l_nodes[0]

    #cl_graph.show()

    explore(cl_graph, d_start)

    n_start = 99
    n_end = 42

    distance, path = shortest_path(
        cl_graph,
        n_start,
        n_end
    )


    print("\nShortest path")
    print(f"From : {n_start}")
    print(f"To   : {n_end}")
    print(f"Cost : {distance}")
    print(f"Path : {path}")

if __name__ == "__main__":
    test_bench()