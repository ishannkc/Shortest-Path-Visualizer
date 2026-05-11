import unittest

from algorithms.dijkstra import dijkstra


ADJ_LIST = {
	"A": [("B", 4), ("C", 2)],
	"B": [("A", 4), ("C", 1), ("D", 5), ("E", 11)],
	"C": [("A", 2), ("B", 1), ("D", 8)],
	"D": [("B", 5), ("C", 8), ("E", 2)],
	"E": [("D", 2), ("B", 11)],
}

class TestDijkstra(unittest.TestCase):
	def test_shortest_path(self):
		result = dijkstra(ADJ_LIST, "A", "E")
		self.assertEqual(result["path"], ["A", "C", "B", "D", "E"])
		self.assertEqual(result["distance"], 10.0)

	def test_same_source_destination(self):
		result = dijkstra(ADJ_LIST, "A", "A")
		self.assertEqual(result["path"], ["A"])
		self.assertEqual(result["distance"], 0.0)

if __name__ == "__main__":
	unittest.main()
