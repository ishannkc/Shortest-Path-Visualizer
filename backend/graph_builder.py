import json
import os
from math import cos, pi, sin

import networkx as nx


def _read_graph_data():
	base_dir = os.path.dirname(os.path.abspath(__file__))
	data_path = os.path.join(base_dir, "..", "data", "graph_data.json")
	data_path = os.path.normpath(data_path)

	if not os.path.exists(data_path):
		raise FileNotFoundError(f"graph_data.json not found at: {data_path}")

	with open(data_path, "r", encoding="utf-8") as file:
		return json.load(file)


def _normalize_positions(nx_graph):
	if nx_graph.number_of_nodes() == 0:
		return {}

	preferred_roots = ["VC Office", "Library Park", "ATM"]
	root = None
	for candidate in preferred_roots:
		if candidate in nx_graph:
			root = candidate
			break

	if root is None:
		root = max(nx_graph.degree, key=lambda item: (item[1], item[0]))[0]

	level_map = nx.single_source_shortest_path_length(nx_graph, root)
	levels = {}
	for node_id, level in level_map.items():
		levels.setdefault(level, []).append(node_id)

	for node_ids in levels.values():
		node_ids.sort()

	orphan_nodes = sorted(set(nx_graph.nodes()) - set(level_map))
	if orphan_nodes:
		levels.setdefault(max(levels.keys(), default=0) + 1, []).extend(orphan_nodes)
		levels[max(levels.keys())].sort()

	max_level = max(levels.keys(), default=0)
	positions = {root: {"x": 0.5, "y": 0.5}}

	if max_level == 0:
		return positions

	max_radius = 0.4
	for level in range(1, max_level + 1):
		nodes_at_level = levels.get(level, [])
		if not nodes_at_level:
			continue

		radius = max_radius * (level / max_level)
		angle_offset = -pi / 2
		angle_step = (2 * pi) / len(nodes_at_level)
		if len(nodes_at_level) == 1:
			positions[nodes_at_level[0]] = {"x": 0.5, "y": 0.5 - radius}
			continue

		for index, node_id in enumerate(nodes_at_level):
			angle = angle_offset + (angle_step * index)
			positions[node_id] = {
				"x": 0.5 + (radius * cos(angle)),
				"y": 0.5 + (radius * sin(angle)),
			}

	return positions


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


def load_graph_data():
	data = _read_graph_data()
	nodes = [node["id"] for node in data.get("nodes", [])]
	nx_graph = nx.Graph()
	nx_graph.add_nodes_from(nodes)

	for edge in data.get("edges", []):
		nx_graph.add_edge(edge["from"], edge["to"], weight=edge["weight"])

	positions = _normalize_positions(nx_graph)
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
