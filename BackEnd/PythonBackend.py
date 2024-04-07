import numpy as np


"""
edges is of the form:
[{"source": 1, "target": 3}, {"source": 2, "target": 3}]
Want to form a laplacian and remove a row and column according to the 2nd node
Weighted laplacian is (AT*C*A) can add this later!
Formula is Kx = f, 
K is laplacian, x is voltages, f is currents
"""


def main(edges, f1):
    edge_list, matrix_dim = clean_edges(edges)
    print("edge_list:", edge_list)
    graph = list_to_dictionary(edge_list)
    if has_path(graph, 1, 2):
        laplacian = edges_to_matrix(edge_list, matrix_dim)  # converts to numpy
        print("laplacian:\n", laplacian)
        inverse_reduced_laplacian = inverse_laplacian(laplacian)
        x = solve_equation(inverse_reduced_laplacian, np.float64(f1), matrix_dim)
        print("Voltages:\n", x.T)
        return x
    return [-1]

def list_to_dictionary(edges):
    graph = {}
    for edge in edges:
        print(edges, edge)
        if edge[0] not in graph:
            graph[edge[0]] = [edge[1]]
        else:
            graph[edge[0]].append(edge[1])
        if edge[1] not in graph:
            graph[edge[1]] = [edge[0]]
        else:
            graph[edge[1]].append(edge[0])
    return graph
    

def has_path(graph, start, end, visited=None):
    # depth first algorithm checks if there exists a path between nodes start and end
    if visited is None:
        visited = set()
    visited.add(start)
    if start == end:
        return True
    for neighbor in graph.get(start, []):
        if neighbor not in visited:
            if has_path(graph, neighbor, end, visited):
                return True
    return False

def clean_edges(edges):
    # Makes sure there are no duplicates and makes the edges all ordered in a list 
    edge_set = set()
    for edge in edges:
        if edge["source"] > edge["target"]:
            edge_set.add((edge["target"], edge["source"], edge["conductance"]))
        else:
            edge_set.add((edge["source"], edge["target"], edge["conductance"]))
    edge_list = sorted(edge_set)
    edge_list = [list(elem) for elem in edge_list]  # so that it is mutable for later

    # Adjusts digits to account for nodes not being connected and hence reducing unnecessary computation
    nodes = set()
    for edge in edge_list:
        nodes = nodes.union({edge[0], edge[1]})
    max_value_node = max(nodes)
    missing_digits = set(range(1, max_value_node + 1)) - nodes
    reduced = False
    while not reduced:
        start = 0
        for digit in missing_digits:
            for n, edge in enumerate(edge_list[start:]):
                changed = False
                if edge[0] > digit:
                    edge_list[n][0] -= 1
                    changed = True
                if edge[1] > digit:
                    edge_list[n][1] -= 1
                    changed = True
                if not changed:
                    start = n
        nodes = set()
        for edge in edge_list:
            nodes = nodes.union({edge[0], edge[1]})
        max_value_node = max(nodes)
        missing_digits = set(range(1, max_value_node + 1)) - nodes
        if not missing_digits:
            reduced = True

    return edge_list, max_value_node, 


def edges_to_matrix(edge_list, matrix_dim):
    # fill in non-diagonals
    laplacian = np.zeros((matrix_dim, matrix_dim))
    for edge in edge_list:
        laplacian[edge[0]-1][edge[1]-1] = -edge[2]
        laplacian[edge[1]-1][edge[0]-1] = -edge[2]
    # fill in diagonals
    for i, row in enumerate(laplacian):
        row_sum = np.sum(row)
        laplacian[i][i] = -row_sum
    return laplacian


def inverse_laplacian(laplacian):
    laplacian1 = np.delete(laplacian, 1, 0)
    laplacian2 = np.delete(laplacian1, 1, 1)
    return np.linalg.inv(laplacian2)


def solve_equation(inv_lap, f1, mat_dim):
    f = np.zeros((mat_dim - 1, 1))
    f[0] = f1
    full_f = np.insert(f, 1, -f1)
    print("f:\n", full_f)
    x_red = np.matmul(inv_lap, f)
    x = np.insert(x_red, 1, 0)
    return x

####################


from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/process_data/", methods=["POST"])
def process_data():
    # Receive the POST request and parse JSON data
    data = request.get_json()

    # Extract the edges dictionary
    edges = data.get("edges")
    f1 = data.get("current1")

    # calculate the voltages given the edge layout and the source current
    if edges:
        voltages = main(edges, f1)
    else:
        voltages = []

    return jsonify(list(voltages))


@app.route("/process_data", methods=["OPTIONS"])  # Handle CORS preflight requests
def handle_options():
    response = app.make_default_options_response()
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:5173/"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "POST"
    return response

if __name__ == "__main__":
    app.run(debug=True)