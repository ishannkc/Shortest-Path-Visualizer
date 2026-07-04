# Shortest Path Visualizer

Kathmandu University Road Network Graph

## Overview

Shortest Path Visualizer is a small web app that compares Dijkstra and Bellman-Ford on a weighted
university road network graph. It exposes a Flask API and serves a lightweight frontend that lets you
select source and destination nodes and view the resulting path and distance.

## Features

- Compare Dijkstra and Bellman-Ford results side by side.
- Visualize the university road network from JSON data.
- Simple Flask API with endpoints for nodes, graph data, and shortest path.
- No external shortest path helpers; algorithms are implemented from scratch.

## Tech Stack

- Python + Flask (API)
- Vanilla HTML/CSS/JS (frontend)
- JSON data source for the road graph

## Project Structure

- `algorithms/`: Dijkstra and Bellman-Ford implementations.
- `backend/`: Flask app and graph builder.
- `data/`: Graph data in JSON format.
- `frontend/`: Static UI assets.
- `tests/`: Unit tests for algorithms.

## Setup

### 1) Create and activate a virtual environment

```powershell
python -m venv .venv
.
.venv\Scripts\Activate.ps1
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

You can start the server directly:

```powershell
python .\backend\app.py
```

Or use the convenience script in the repo root:

```powershell
.
.\run.ps1
```

The app runs at:

- http://127.0.0.1:5000/

## API Endpoints

- `GET /` - Serve the frontend.
- `GET /frontend/<file>` - Serve static frontend files.
- `GET /nodes` - List all node names.
- `GET /graph` - Return the full graph JSON data.
- `GET /shortest-path?src=A&dst=B` - Compute shortest paths using both algorithms.

## Notes

- All node names come from the graph data file.
- The Flask app serves the frontend, so you only need to run the backend server.
