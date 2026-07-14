import os
import sys

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.normpath(os.path.join(BASE_DIR, ".."))
FRONTEND_DIR = os.path.join(ROOT_DIR, "frontend")
if ROOT_DIR not in sys.path:
	sys.path.insert(0, ROOT_DIR)

from algorithms.bellman_ford import bellman_ford
from algorithms.dijkstra import dijkstra
from backend.graph_builder import load_graph, load_vehicle_graph, load_vehicle_edge_list, load_graph_data, PARKING_NODES


app = Flask(__name__)
CORS(app)

ADJ_LIST, EDGE_LIST, NODES, _ = load_graph()
VEHICLE_ADJ_LIST = load_vehicle_graph()
VEHICLE_EDGE_LIST = load_vehicle_edge_list()


@app.get("/graph")
def get_graph():
	return jsonify(load_graph_data())


@app.get("/")
def serve_index():
	return send_from_directory(FRONTEND_DIR, "index.html")


@app.get("/frontend/<path:filename>")
def serve_frontend_file(filename):
	return send_from_directory(FRONTEND_DIR, filename)


@app.get("/nodes")
def get_nodes():
	return jsonify(NODES)


def find_vehicle_path(src, dst):
	direct = dijkstra(VEHICLE_ADJ_LIST, src, dst)
	if direct["distance"] >= 0:
		return {
			"path": direct["path"],
			"distance": direct["distance"],
			"parking": None,
			"drive_distance": direct["distance"],
			"walk_distance": 0,
			"drive_path": direct["path"],
			"walk_path": [],
		}

	best = {"path": [], "distance": -1, "parking": None, "drive_path": [], "walk_path": []}

	for parking in PARKING_NODES:
		drive = dijkstra(VEHICLE_ADJ_LIST, src, parking)
		if drive["distance"] < 0:
			continue
		walk = dijkstra(ADJ_LIST, parking, dst)
		if walk["distance"] < 0:
			continue
		total = round(drive["distance"] + walk["distance"], 4)
		if best["distance"] < 0 or walk["distance"] < best.get("walk_distance", float("inf")):
			combined_path = drive["path"] + walk["path"][1:]
			best = {
				"path": combined_path,
				"distance": total,
				"parking": parking,
				"drive_distance": drive["distance"],
				"walk_distance": walk["distance"],
				"drive_path": drive["path"],
				"walk_path": walk["path"],
			}

	return best


@app.get("/shortest-path")
def get_shortest_path():
	src = request.args.get("src")
	dst = request.args.get("dst")
	mode = request.args.get("mode", "walking")

	if not src or not dst:
		return jsonify({"error": "src and dst are required"}), 400

	if src not in NODES:
		return jsonify({"error": f"Invalid node name: {src}"}), 400
	if dst not in NODES:
		return jsonify({"error": f"Invalid node name: {dst}"}), 400

	if mode == "vehicle":
		result = find_vehicle_path(src, dst)
		return jsonify({"vehicle": result})

	d_result = dijkstra(ADJ_LIST, src, dst)
	b_result = bellman_ford(EDGE_LIST, NODES, src, dst)
	return jsonify({"dijkstra": d_result, "bellman_ford": b_result})


def _run_algorithm(algorithm, adj_list, edge_list, nodes, src, dst):
	if algorithm == "dijkstra":
		return dijkstra(adj_list, src, dst)
	return bellman_ford(edge_list, nodes, src, dst)


def visualize_vehicle_path(src, dst, algorithm):
	direct = _run_algorithm(algorithm, VEHICLE_ADJ_LIST, VEHICLE_EDGE_LIST, NODES, src, dst)
	if direct.get("path") and direct.get("distance", -1) >= 0:
		return direct

	best = None
	for parking in PARKING_NODES:
		drive = _run_algorithm(algorithm, VEHICLE_ADJ_LIST, VEHICLE_EDGE_LIST, NODES, src, parking)
		if not drive.get("path") or drive.get("distance", -1) < 0:
			continue

		walk = _run_algorithm(algorithm, ADJ_LIST, EDGE_LIST, NODES, parking, dst)
		if not walk.get("path") or walk.get("distance", -1) < 0:
			continue

		if best is None or walk["distance"] < best["walk_distance"]:
			best = {
				"path": drive["path"] + walk["path"][1:],
				"distance": round(drive["distance"] + walk["distance"], 4),
				"steps": drive["steps"] + walk["steps"],
				"visited_nodes": drive["visited_nodes"] + walk["visited_nodes"],
				"explored_edges": drive["explored_edges"] + walk["explored_edges"],
				"step_edges": drive["step_edges"] + walk["step_edges"],
				"parking": parking,
				"drive_distance": drive["distance"],
				"walk_distance": walk["distance"],
				"drive_path": drive["path"],
				"walk_path": walk["path"],
			}

	if best:
		return best

	return {
		"path": [], "distance": -1, "steps": 0,
		"visited_nodes": [], "explored_edges": [], "step_edges": [],
	}


@app.get("/visualize")
def get_visualization():
	src = request.args.get("src")
	dst = request.args.get("dst")
	algorithm = request.args.get("algorithm")
	mode = request.args.get("mode", "walking")

	if not src or not dst:
		return jsonify({"error": "src and dst are required"}), 400
	if not algorithm:
		return jsonify({"error": "algorithm parameter is required"}), 400

	if src not in NODES:
		return jsonify({"error": f"Invalid node name: {src}"}), 400
	if dst not in NODES:
		return jsonify({"error": f"Invalid node name: {dst}"}), 400

	if mode == "vehicle":
		result = visualize_vehicle_path(src, dst, algorithm)
	elif algorithm == "dijkstra":
		result = dijkstra(ADJ_LIST, src, dst)
	elif algorithm == "bellman_ford":
		result = bellman_ford(EDGE_LIST, NODES, src, dst)
	else:
		return jsonify({"error": f"Unknown algorithm: {algorithm}"}), 400

	return jsonify(result)


if __name__ == "__main__":
	app.run(debug=True, port=5000)
