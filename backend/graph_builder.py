import json
import os

import networkx as nx


def _read_graph_data():
	base_dir = os.path.dirname(os.path.abspath(__file__))
	data_path = os.path.join(base_dir, "..", "data", "graph_data.json")
	data_path = os.path.normpath(data_path)

	if not os.path.exists(data_path):
		raise FileNotFoundError(f"graph_data.json not found at: {data_path}")

	with open(data_path, "r", encoding="utf-8") as file:
		return json.load(file)


def _normalize_positions(node_data):
	if not node_data:
		return {}

	x_values = [node["x"] for node in node_data if "x" in node and "y" in node]
	y_values = [node["y"] for node in node_data if "x" in node and "y" in node]
	if not x_values or not y_values:
		return {}

	min_x = min(x_values)
	max_x = max(x_values)
	min_y = min(y_values)
	max_y = max(y_values)

	x_span = max(max_x - min_x, 1)
	y_span = max(max_y - min_y, 1)
	padding = 0.03
	usable_space = 1 - (padding * 2)

	return {
		node["id"]: {
			"x": padding + (((node["x"] - min_x) / x_span) * usable_space),
			"y": padding + (((node["y"] - min_y) / y_span) * usable_space),
		}
		for node in node_data
		if "id" in node and "x" in node and "y" in node
	}


def load_graph():
	data = _read_graph_data()

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


ONE_WAY_VEHICLE_EDGES = {
	("VC Office", "Canteen"),
	("Canteen", "Block 6"),
	("Block 6", "Fountain"),
	("Fountain", "Semi-circle Park"),
	("Semi-circle Park", "Cafeteria"),
	("Cafeteria", "VC Office"),
}


def load_vehicle_graph():
	data = _read_graph_data()
	nodes = [node["id"] for node in data.get("nodes", [])]
	adj_list = {node_id: [] for node_id in nodes}

	for edge in data.get("edges", []):
		if edge.get("type") != "vehicle":
			continue
		u = edge["from"]
		v = edge["to"]
		weight = edge["weight"]

		if (u, v) in ONE_WAY_VEHICLE_EDGES:
			adj_list[u].append((v, weight))
		elif (v, u) in ONE_WAY_VEHICLE_EDGES:
			adj_list[v].append((u, weight))
		else:
			adj_list[u].append((v, weight))
			adj_list[v].append((u, weight))

	return adj_list


PARKING_NODES = ["Parking 1", "Parking 2", "Parking 3"]


def load_graph_data():
	data = _read_graph_data()
	node_data = data.get("nodes", [])
	nodes = [node["id"] for node in node_data]
	positions = _normalize_positions(node_data)
	return {
		"nodes": [
			{
				"id": node_id,
				"x": positions.get(node_id, {}).get("x", 0.5),
				"y": positions.get(node_id, {}).get("y", 0.5),
			}
			for node_id in nodes
		],
		"edges": data.get("edges", []),
	}
