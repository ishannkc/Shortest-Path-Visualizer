import heapq


def dijkstra(adj_list, source, destination):
	if source not in adj_list or destination not in adj_list:
		return {"path": [], "distance": -1, "steps": 0}

	dist = {node: float("inf") for node in adj_list}
	prev = {node: None for node in adj_list}
	visited = set()
	heap = [(0, source)]
	dist[source] = 0
	steps = 0

	while heap:
		cost, node = heapq.heappop(heap)
		if node in visited:
			continue
		visited.add(node)

		if node == destination:
			break

		for neighbor, weight in adj_list.get(node, []):
			tentative = dist[node] + weight
			if tentative < dist[neighbor]:
				dist[neighbor] = tentative
				prev[neighbor] = node
				heapq.heappush(heap, (tentative, neighbor))
				steps += 1

	if dist[destination] == float("inf"):
		return {"path": [], "distance": -1, "steps": 0}

	path = []
	current = destination
	while current is not None:
		path.append(current)
		if current == source:
			break
		current = prev[current]

	if not path or path[-1] != source:
		return {"path": [], "distance": -1, "steps": 0}

	path.reverse()
	return {
		"path": path,
		"distance": round(dist[destination], 4),
		"steps": steps,
	}
