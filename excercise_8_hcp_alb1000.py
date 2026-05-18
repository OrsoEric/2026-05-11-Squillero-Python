from math import sqrt
from itertools import combinations
import re
from collections import deque

from pathlib import Path

#from graph_alist import cl_graph

from excercise_7_graph_dict import Cl_graph

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
    with open(filename) as data:
        whole_file = data.read()

    name = extract_field('NAME', whole_file)
    comment = extract_field('COMMENT', whole_file)
    format = extract_field('EDGE_WEIGHT_TYPE', whole_file)
    if not format:
        format = extract_field('EDGE_DATA_FORMAT', whole_file)
    print(name)
    print(comment)

    n_cities = int(extract_field('DIMENSION', whole_file))
    cl_graph = Cl_graph()
    if format == 'EXPLICIT':
        data = deque(int(d) for d in extract_section('EDGE_WEIGHT_SECTION', whole_file).split())
        if extract_field('EDGE_WEIGHT_FORMAT', whole_file) == 'LOWER_DIAG_ROW':
            for c1 in range(n_cities):
                for c2 in range(c1):
                    w = data.popleft()
                    cl_graph.add_link_one_way(c1, c2, w)
                    cl_graph.add_link_one_way(c2, c1, w)
                assert data.popleft() == 0
        elif extract_field('EDGE_WEIGHT_FORMAT', whole_file) == 'UPPER_ROW':
            for c1 in range(n_cities):
                for c2 in range(1, n_cities - c1):
                    w = data.popleft()
                    cl_graph.add_link_one_way(c1, c2, w)
                    cl_graph.add_link_one_way(c2, c1, w)
    elif format == 'ATT':
        cities = list()
        for l in extract_section('NODE_COORD_SECTION', whole_file).split('\n'):
            if not l.strip():
                continue
            _, x, y = map(int, l.split())
            cities.append((x, y))
        for c1, c2 in combinations(range(n_cities), r=2):
            d = sqrt((cities[c1][0] - cities[c2][0]) ** 2 + (cities[c1][1] - cities[c2][1]) ** 2)
            cl_graph.add_link_one_way(c1, c2, d)
            cl_graph.add_link_one_way(c2, c1, d)
    elif format == 'EDGE_LIST':
        for l in extract_section('EDGE_DATA_SECTION', whole_file).split('\n'):
            if not l.strip():
                continue
            n1, n2 = map(int, l.split())

            cl_graph.add_link_one_way(n1 - 1, n2 - 1, 1)
            cl_graph.add_link_one_way(n2 - 1, n1 - 1, 1)
    else:
        assert False, "Can't parse cl_graph!"

    return cl_graph


def test_bench():
    print(f"file: {C_S_FILE}")
    cl_graph = read_graph(C_S_FILE)
    cl_graph.show()



if __name__ == "__main__":
    test_bench()