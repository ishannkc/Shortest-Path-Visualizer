# Shortest Path Visualizer

Shortest Path Visualizer is a web app that compares **Dijkstra** and **Bellman-Ford** on a weighted
university road network graph. It supports both **walking** and **vehicle** transport modes, with
parking-lot integration for multi-modal routing. The app exposes a Flask API and serves a lightweight
frontend that lets you select source and destination nodes, view the resulting path and distance,
and watch step-by-step algorithm visualizations.

## Features

### Routing
- **Walking mode** — shortest path across pedestrian edges using Dijkstra and Bellman-Ford.
- **Vehicle mode** — shortest path across vehicle-accessible roads; if no direct vehicle route exists,
  finds the shortest combined drive + walk path via the nearest parking node.
- **One-way roads** — a set of 6 edges form a one-way vehicle loop (VC Office → Canteen → Block 6 →
  Fountain → Semi-circle Park → Cafeteria → VC Office).

### Visualization
- Step-by-step animation showing visited nodes, explored edges, and the final shortest path.
- Both algorithms can be visualized side by side.
- Vehicle mode merges drive and walk segments into a single visualization sequence.

### UI
- Interactive SVG graph with zoom, pan, and responsive layout.
- Source/destination pickers with clear visual highlights.
- Direction panel showing the full path with parking stops distinguished.
- Analytics table with path length, distance, steps, and algorithm-specific metrics.
- Dynamic legend that reveals the parking indicator when a parking transfer is used.

## Tech Stack

- Python + Flask (API, CORS enabled)
- Vanilla HTML/CSS/JS (frontend)
- JSON data source for the road graph
- NetworkX (internal graph utilities)

## Project Structure

```
Shortest-Path-Visualizer/
├── algorithms/          # Dijkstra and Bellman-Ford implementations
├── backend/             # Flask app and graph builder
│   ├── app.py           # API entry point
│   └── graph_builder.py # Graph loading and vehicle graph construction
├── data/                # Graph data in JSON format
│   └── graph_data.json  # Nodes, edges, coordinates, and edge types
├── frontend/            # Static UI assets
│   └── index.html       # Single-page frontend
├── tests/               # Unit tests for algorithms
├── requirements.txt     # Python dependencies
├── run.ps1              # Convenience startup script
└── README.md
```

## Setup

### 1) Create and activate a virtual environment

```powershell
python -m venv .venv
.\\.venv\Scripts\Activate.ps1
```

### 2) Install dependencies

```powershell
pip install -r requirements.txt
```

If you do not have a `requirements.txt` yet, install the core packages:

```powershell
pip install flask flask-cors
```

### 3) Run the web app

Start the server directly:

```powershell
python .\backend\app.py
```

Or use the convenience script in the repo root:

```powershell
.\run.ps1
```

The app runs at:

- http://127.0.0.1:5000/

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Serve the frontend |
| GET | `/frontend/<file>` | Serve static frontend files |
| GET | `/nodes` | List all node names |
| GET | `/graph` | Return the full graph JSON data |
| GET | `/shortest-path?src=A&dst=B&mode=<walking\|vehicle>` | Compute shortest path (optionally in vehicle mode) |
| GET | `/visualize?src=A&dst=B&algorithm=<dijkstra\|bellman_ford>&mode=<walking\|vehicle>` | Step-by-step visualization data |

## Notes

- All node names come from the graph data file `data/graph_data.json`.
- Edges are classified with `"type": "vehicle"` for vehicle-accessible roads or omitted for walking paths.
- Parking nodes are: Parking 1–3, Mechanical Workshop, NTIC Research Center, Boys Hostel, Block 9,
  Civil Engineering Block, Pharmacy Block, Mesh Canteen, Buspark, Environment Block, School of Law.
- The Flask app serves the frontend, so you only need to run the backend server.
