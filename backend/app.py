import json
import os
import sys

from flask import Flask, jsonify, request
from flask_cors import CORS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.normpath(os.path.join(BASE_DIR, ".."))
if ROOT_DIR not in sys.path:
	sys.path.insert(0, ROOT_DIR)

from algorithms.bellman_ford import bellman_ford
from algorithms.dijkstra import dijkstra
from backend.graph_builder import load_graph


app = Flask(__name__)
CORS(app)

ADJ_LIST, EDGE_LIST, NODES, _ = load_graph()


@app.get("/graph")
def get_graph():
	data_path = os.path.normpath(os.path.join(BASE_DIR, "..", "data", "graph_data.json"))
	with open(data_path, "r", encoding="utf-8") as file:
		data = json.load(file)
	return jsonify(data)


@app.get("/nodes")
def get_nodes():
	return jsonify(NODES)


@app.get("/shortest-path")
def get_shortest_path():
	src = request.args.get("src")
	dst = request.args.get("dst")

	if not src or not dst:
		return jsonify({"error": "src and dst are required"}), 400

	if src not in NODES:
		return jsonify({"error": f"Invalid node name: {src}"}), 400
	if dst not in NODES:
		return jsonify({"error": f"Invalid node name: {dst}"}), 400

	d_result = dijkstra(ADJ_LIST, src, dst)
	b_result = bellman_ford(EDGE_LIST, NODES, src, dst)
	return jsonify({"dijkstra": d_result, "bellman_ford": b_result})


if __name__ == "__main__":
	app.run(debug=True, port=5000)
