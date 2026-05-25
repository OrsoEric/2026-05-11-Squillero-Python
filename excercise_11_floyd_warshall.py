"""
Floyd Warshall

find all best distances between all pair of nodes

complexity node^3

"""

from lib.cl_graph_dict import Cl_graph

class lib_numpy:
    from numpy import empty, nan


def find_all_shortest(i_cl_graph : Cl_graph) -> bool:

    #how many nodes
    n_node : int = i_cl_graph.num_node
    print(f"num nodes: {n_node}")
    #create an array of costs
    lnn_cost = lib_numpy.empty((n_node, n_node), dtype=float)
    #set cost to infinite
    lnn_cost.fill(lib_numpy.nan)

    #take all the links and write their cost as starting point of the cost matrix
    #iterate link and indexed nodes
    for t_nnn in i_cl_graph.iter_link_node_index():
        #unpack
        n_index_start = t_nnn[0]
        n_index_end = t_nnn[1]
        n_cost = t_nnn[2]
        #assign
        lnn_cost[n_index_start][n_index_end] = n_cost
        

    #for all links, initialize cost
    

    #distance of a node to itself is zero
    for n_node_index in range(n_node):
        lnn_cost[n_node_index][n_node_index] = 0

    print(lnn_cost)

    return False #OK



def test_bench():
    print("shaka")

    cl_graph = Cl_graph()

    # Rail distances (approximate, km)
    cl_graph.add_link_two_way("London", "Paris", 450)
    cl_graph.add_link_two_way("London", "Brussels", 320)
    cl_graph.add_link_two_way("Paris", "Brussels", 300)
    cl_graph.add_link_two_way("Brussels", "Amsterdam", 200)
    cl_graph.add_link_two_way("Amsterdam", "Berlin", 650)
    cl_graph.add_link_two_way("Paris", "Berlin", 1050)

    print("Rail network g_d_graph (edges):")
    cl_graph.show()

    find_all_shortest( cl_graph )




if __name__ == "__main__":
    test_bench()
