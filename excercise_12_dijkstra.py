from pathlib import Path

from lib.cl_graph_dict import Cl_graph

class lib_numpy:
    from numpy import empty, inf

#from collections import deque

from lib.cl_priority_binary_tree import Cl_priority_binary_tree


def dummy_graph( i_cl_graph ):
     # Rail distances (approximate, km)
    i_cl_graph.add_link_two_way("London", "Paris", 450)
    i_cl_graph.add_link_two_way("London", "Brussels", 320)
    i_cl_graph.add_link_two_way("Paris", "Brussels", 300)
    i_cl_graph.add_link_two_way("Brussels", "Amsterdam", 200)
    i_cl_graph.add_link_two_way("Amsterdam", "Berlin", 650)
    i_cl_graph.add_link_two_way("Paris", "Berlin", 1050)
    return False


def dijkstra( i_cl_graph : Cl_graph, i_s_start : str, i_s_end : str ) -> bool:

    cl_graph = i_cl_graph

    cl_frontier = Cl_priority_binary_tree()

    #compute the indexes of the nodes
    i_n_start_index = cl_graph.get_node_index(i_s_start)
    print(f"Start {i_s_start} {i_n_start_index}")
    i_n_end_index = cl_graph.get_node_index(i_s_end)
    print(f"Start {i_s_end} {i_n_end_index}")

    #create a vector of distance, one per node
    ln_cost = lib_numpy.empty((cl_graph.num_node), dtype=float)   
    #distance is infinite to all nodes
    ln_cost.fill(lib_numpy.inf)
    #distance to itself is zero
    ln_cost[i_n_start_index] = 0
    print(f"Cost vector {ln_cost}")

    #create the frontier
    l_link_start= cl_graph.get_neighbour(i_s_start)
    for s_node_end, n_link_cost in l_link_start:
        
        #append right
        cl_frontier.push( s_node_end, n_link_cost) 
        #index of the destination of this link
        i_n_index = cl_graph.get_node_index(s_node_end)
        ln_cost[i_n_index] = n_link_cost

    print(f"Cost vector after frontier  {ln_cost}")

    print(f"Frontier: {l_link_start}")

    while len(cl_frontier) > 0:
        s_node_name, n_link_length = cl_frontier.pop_lowest()
        print(f"POP {s_node_name} {n_link_length}")

    



    return False #OK

def test_bench():
    print("shaka")

    cl_graph = Cl_graph()



   
    
    dummy_graph(cl_graph)

    #load_graph_from_file( Path("data","Salario.dat"), cl_graph )

    cl_graph.show()


    dijkstra(cl_graph, "London", "Berlin")



if __name__ == "__main__":
    test_bench()
