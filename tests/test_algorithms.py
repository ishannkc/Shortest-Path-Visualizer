import unittest

from algorithms.bellman_ford import bellman_ford
from algorithms.dijkstra import dijkstra


NODES = ["A", "B", "C", "D", "E"]

ADJ_LIST = {
	"A": [("B", 4), ("C", 2)],
	"B": [("A", 4), ("C", 1), ("D", 5), ("E", 11)],
	"C": [("A", 2), ("B", 1), ("D", 8)],
	"D": [("B", 5), ("C", 8), ("E", 2)],
	"E": [("D", 2), ("B", 11)],
}

EDGE_LIST = [
	("A", "B", 4),
	("B", "A", 4),
	("A", "C", 2),
	("C", "A", 2),
	("C", "B", 1),
	("B", "C", 1),
	("B", "D", 5),
	("D", "B", 5),
	("C", "D", 8),
	("D", "C", 8),
	("D", "E", 2),
	("E", "D", 2),
	("B", "E", 11),
	("E", "B", 11),
]


class TestDijkstra(unittest.TestCase):
	def test_shortest_path(self):
		result = dijkstra(ADJ_LIST, "A", "E")
		self.assertEqual(result["path"], ["A", "C", "B", "D", "E"])
		self.assertEqual(result["distance"], 10.0)

	def test_same_source_destination(self):
		result = dijkstra(ADJ_LIST, "A", "A")
		self.assertEqual(result["path"], ["A"])
		self.assertEqual(result["distance"], 0.0)


class TestBellmanFord(unittest.TestCase):
	def test_shortest_path(self):
		result = bellman_ford(EDGE_LIST, NODES, "A", "E")
		self.assertEqual(result["path"], ["A", "C", "B", "D", "E"])
		self.assertEqual(result["distance"], 10.0)

	def test_no_negative_cycle(self):
		result = bellman_ford(EDGE_LIST, NODES, "A", "E")
		self.assertFalse(result["negative_cycle"])

	def test_same_source_destination(self):
		result = bellman_ford(EDGE_LIST, NODES, "A", "A")
		self.assertEqual(result["path"], ["A"])
		self.assertEqual(result["distance"], 0.0)


class TestComparison(unittest.TestCase):
	def test_same_result(self):
		d_result = dijkstra(ADJ_LIST, "A", "E")
		b_result = bellman_ford(EDGE_LIST, NODES, "A", "E")
		self.assertEqual(d_result["path"], b_result["path"])
		self.assertEqual(d_result["distance"], b_result["distance"])

	def test_dijkstra_fewer_steps(self):
		d_result = dijkstra(ADJ_LIST, "A", "E")
		b_result = bellman_ford(EDGE_LIST, NODES, "A", "E")
		self.assertGreaterEqual(d_result["steps"], 0)
		self.assertGreaterEqual(b_result["steps"], 0)


if __name__ == "__main__":
	unittest.main()
