"""
Floyd Warshall

find all best distances between all pair of nodes

complexity node^3

"""

from pathlib import Path

from lib.cl_graph_dict import Cl_graph

class lib_numpy:
    from numpy import empty, inf

from itertools import product
from tqdm.auto import tqdm

def find_all_shortest(i_cl_graph : Cl_graph) -> bool:

    #how many nodes
    n_node : int = i_cl_graph.num_node
    print(f"num nodes: {n_node}")
    #create an array of costs
    lnn_cost = lib_numpy.empty((n_node, n_node), dtype=float)
    #set cost to infinite
    lnn_cost.fill(lib_numpy.inf)

    #take all the links and write their cost as starting point of the cost matrix
    #iterate link and indexed nodes
    for t_nnn in i_cl_graph.iter_link_node_index():
        #unpack
        n_index_start = t_nnn[0]
        n_index_end = t_nnn[1]
        n_cost = t_nnn[2]
        #assign
        lnn_cost[n_index_start][n_index_end] = n_cost
        
    #distance of a node to itself is zero
    for n_node_index in range(n_node):
        lnn_cost[n_node_index][n_node_index] = 0

    print("Starting cost matrix")
    print(lnn_cost)


            
    for n_k, n_i, n_j in tqdm(product(range(n_node), repeat=3)):
        if lnn_cost[n_i][n_j] > lnn_cost[n_i][n_k] + lnn_cost[n_k][n_j]:
            #print(f"update cost {n_i}{n_j}")
            lnn_cost[n_i][n_j] = lnn_cost[n_i][n_k] + lnn_cost[n_k][n_j]
    
    print("Final cost matrix")
    print(lnn_cost)

    return lnn_cost

# ------------------------------------------------------------
# LOADER FOR /data/salario.dat
# ------------------------------------------------------------

def load_graph_from_file(i_s_path, cl_graph):
    """
    File format:
        <idA> <idB> <weight>

    """
    with open(i_s_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            parts = line.split()
            if len(parts) != 3:
                continue

            a_id = int(parts[0])
            b_id = int(parts[1])
            weight = float(parts[2])

            a_name = f"Node{a_id}"
            b_name = f"Node{b_id}"

            cl_graph.add_link_two_way(a_name, b_name, weight)

    return cl_graph


def dummy_graph( i_cl_graph ):
     # Rail distances (approximate, km)
    i_cl_graph.add_link_two_way("London", "Paris", 450)
    i_cl_graph.add_link_two_way("London", "Brussels", 320)
    i_cl_graph.add_link_two_way("Paris", "Brussels", 300)
    i_cl_graph.add_link_two_way("Brussels", "Amsterdam", 200)
    i_cl_graph.add_link_two_way("Amsterdam", "Berlin", 650)
    i_cl_graph.add_link_two_way("Paris", "Berlin", 1050)
    return False

def save_csv(i_s_path, i_lln_array):
    with open(i_s_path, "w") as f:
        for ln_row in i_lln_array:
            line = ",".join(str(x) for x in ln_row)
            f.write(line + "\n")

def test_bench():
    print("shaka")

    cl_graph = Cl_graph()



   
    
    #dummy_graph(cl_graph)

    load_graph_from_file( Path("data","Salario.dat"), cl_graph )


    # try linear graph

    print("Rail network g_d_graph (edges):")
    cl_graph.show()

    lln_distance = find_all_shortest( cl_graph )

    save_csv(Path("data","Salario.csv"), lln_distance)


if __name__ == "__main__":
    test_bench()
