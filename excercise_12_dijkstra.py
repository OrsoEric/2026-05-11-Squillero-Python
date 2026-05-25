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

    


    #create the frontier
    l_link_start= cl_graph.get_neighbour(i_s_start)
    for st_link in l_link_start:
        #append right
        cl_frontier.push( st_link[0], st_link[1]) 

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
