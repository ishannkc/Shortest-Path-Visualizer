def bellman_ford(edge_list, nodes, source, destination):
	if source not in nodes or destination not in nodes:
		return {
			"path": [], "distance": -1, "steps": 0,
			"negative_cycle": False, "visited_nodes": [], "explored_edges": [],
			"step_edges": [],
		}

	dist = {node: float("inf") for node in nodes}
	prev = {node: None for node in nodes}
	steps = 0
	visited_nodes = []
	explored_edges = []
	step_edges = []

	dist[source] = 0
	visited_nodes.append(source)
	step_edges.append([])
	vertices = len(nodes)

	for _ in range(vertices - 1):
		updated = set()
		round_edges = []
		for u, v, weight in edge_list:
			if dist[u] != float("inf") and dist[u] + weight < dist[v]:
				dist[v] = dist[u] + weight
				prev[v] = u
				explored_edges.append([u, v])
				round_edges.append([u, v])
				updated.add(v)
				steps += 1
		for node in updated:
			visited_nodes.append(node)
		if round_edges:
			step_edges.append(round_edges)

	for u, v, weight in edge_list:
		if dist[u] != float("inf") and dist[u] + weight < dist[v]:
			return {
				"path": [], "distance": -1, "steps": steps,
				"negative_cycle": True, "visited_nodes": visited_nodes,
				"explored_edges": explored_edges, "step_edges": step_edges,
			}

	if dist[destination] == float("inf"):
		return {
			"path": [], "distance": -1, "steps": steps,
			"negative_cycle": False, "visited_nodes": visited_nodes,
			"explored_edges": explored_edges, "step_edges": step_edges,
		}

	path = []
	current = destination
	while current is not None:
		path.append(current)
		if current == source:
			break
		current = prev[current]

	if not path or path[-1] != source:
		return {
			"path": [], "distance": -1, "steps": steps,
			"negative_cycle": False, "visited_nodes": visited_nodes,
			"explored_edges": explored_edges, "step_edges": step_edges,
		}

	path.reverse()
	return {
		"path": path,
		"distance": round(dist[destination], 4),
		"steps": steps,
		"negative_cycle": False,
		"visited_nodes": visited_nodes,
		"explored_edges": explored_edges,
		"step_edges": step_edges,
	}
