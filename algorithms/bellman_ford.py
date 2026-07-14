def bellman_ford(edge_list, nodes, source, destination):
	if source not in nodes or destination not in nodes:
		return {"path": [], "distance": -1, "steps": 0, "negative_cycle": False, "visited_nodes": []}

	dist = {node: float("inf") for node in nodes}
	prev = {node: None for node in nodes}
	steps = 0
	visited_nodes = []

	dist[source] = 0
	visited_nodes.append(source)
	vertices = len(nodes)

	for _ in range(vertices - 1):
		updated = set()
		for u, v, weight in edge_list:
			if dist[u] != float("inf") and dist[u] + weight < dist[v]:
				dist[v] = dist[u] + weight
				prev[v] = u
				updated.add(v)
				steps += 1
		for node in updated:
			visited_nodes.append(node)

	for u, v, weight in edge_list:
		if dist[u] != float("inf") and dist[u] + weight < dist[v]:
			return {
				"path": [], "distance": -1, "steps": steps,
				"negative_cycle": True, "visited_nodes": visited_nodes,
			}

	if dist[destination] == float("inf"):
		return {
			"path": [], "distance": -1, "steps": steps,
			"negative_cycle": False, "visited_nodes": visited_nodes,
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
		}

	path.reverse()
	return {
		"path": path,
		"distance": round(dist[destination], 4),
		"steps": steps,
		"negative_cycle": False,
		"visited_nodes": visited_nodes,
	}
