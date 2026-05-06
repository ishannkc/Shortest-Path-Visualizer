import json
import os

import networkx as nx


def load_graph():
	base_dir = os.path.dirname(os.path.abspath(__file__))
	data_path = os.path.join(base_dir, "..", "data", "graph_data.json")
	data_path = os.path.normpath(data_path)

	if not os.path.exists(data_path):
		raise FileNotFoundError(f"graph_data.json not found at: {data_path}")

	with open(data_path, "r", encoding="utf-8") as file:
		data = json.load(file)

	nodes = [node["id"] for node in data.get("nodes", [])]
	adj_list = {node_id: [] for node_id in nodes}
	edge_list = []
	nx_graph = nx.Graph()

	nx_graph.add_nodes_from(nodes)

	for edge in data.get("edges", []):
		u = edge["from"]
		v = edge["to"]
		weight = edge["weight"]

		adj_list[u].append((v, weight))
		adj_list[v].append((u, weight))
		edge_list.append((u, v, weight))
		edge_list.append((v, u, weight))
		nx_graph.add_edge(u, v, weight=weight)

	return adj_list, edge_list, nodes, nx_graph
