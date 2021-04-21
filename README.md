# PythonGraph
An implementation of a connected graph in Python.

This repository contains the necessary tools for created a simple interconnected graph in Python.

An example of creating a generic graph:
```python
node1 = GraphNode(label='NODE1', value=10)
node2 = GraphNode(label='NODE2', value=15)

"""
In this example both node1 and node2 have a contains dictionary
that has a value entry in it.
"""

graph = Graph()
graph.add_vertex(node1)
graph.add_vertex(node2)
graph.add_edge(node1, node2)
```

Or to add a directional edge:
```python
graph.add_edge(node1, node2, directional=True)
```

Or to make it a weighted edge:
```python
graph.add_edge(node1, node2, e=25.2)
```

An example of creating a Graph from a csv:
```python
path = os.path.join(sys.path[0], Path(
    "data/csv-data/airports_new.csv"))

graph = graph_from_geodata_csv(path)
```
