from regraph import NXGraph, Rule
from regraph import plot_graph, plot_instance, plot_rule



# Create an empty graph object
graph = NXGraph()

# Add a list of nodes, optionally with attributes
graph.add_nodes_from(
    [
        'IBM',
        'Google',

])

# Add a list of edges, optionally with attributes
graph.add_edges_from([
    ("IBM", "Google", {"type": "organisation"}),

])


print("List of nodes: ")
for n, attrs in graph.nodes(data=True):
    print("\t", n, attrs)
print("List of edges: ")
for s, t, attrs in graph.edges(data=True):
    print("\t{}->{}".format(s, t), attrs)


positioning = plot_graph(graph)