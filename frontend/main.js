const API_BASE = "http://localhost:5000";

let network = null;
let edgesDataSet = null;

function ensureVisNetwork() {
	if (window.vis) {
		return Promise.resolve();
	}

	return new Promise((resolve, reject) => {
		const script = document.createElement("script");
		script.src = "https://unpkg.com/vis-network@9.1.2/dist/vis-network.min.js";
		script.onload = () => resolve();
		script.onerror = () => reject(new Error("Failed to load vis-network library"));
		document.head.appendChild(script);
	});
}

function setError(message) {
	const errorEl = document.getElementById("error-msg");
	if (message) {
		errorEl.textContent = message;
		errorEl.style.display = "inline";
	} else {
		errorEl.textContent = "";
		errorEl.style.display = "none";
	}
}

function findEdgeId(fromNode, toNode) {
	const edges = edgesDataSet.get();
	const match = edges.find(
		(edge) =>
			(edge.from === fromNode && edge.to === toNode) ||
			(edge.from === toNode && edge.to === fromNode)
	);
	return match ? match.id : null;
}

function updateComparison(dResult) {
	document.getElementById("cmp-path-d").textContent = dResult.path.join(" → ");
	document.getElementById("cmp-distance-d").textContent = `${dResult.distance} km`;
	document.getElementById("cmp-steps-d").textContent = `${dResult.steps} relaxations`;
	document.getElementById("cmp-time-d").textContent = "O((V+E) log V)";
}

document.addEventListener("DOMContentLoaded", () => {
	const srcSelect = document.getElementById("src-select");
	const dstSelect = document.getElementById("dst-select");
	const runButton = document.getElementById("run-btn");

	ensureVisNetwork()
		.then(() => Promise.all([fetch(`${API_BASE}/graph`), fetch(`${API_BASE}/nodes`)]))
		.then(async ([graphRes, nodesRes]) => {
			if (!graphRes.ok) {
				throw new Error("Failed to load graph data");
			}
			if (!nodesRes.ok) {
				throw new Error("Failed to load nodes");
			}

			const graphData = await graphRes.json();
			const nodes = await nodesRes.json();

			const visNodes = graphData.nodes.map((node) => ({
				id: node.id,
				label: node.id,
			}));
			const visEdges = graphData.edges.map((edge, index) => ({
				id: index,
				from: edge.from,
				to: edge.to,
				label: String(edge.weight),
				color: "#848484",
			}));

			const container = document.getElementById("graph-container");
			edgesDataSet = new vis.DataSet(visEdges);
			const data = {
				nodes: new vis.DataSet(visNodes),
				edges: edgesDataSet,
			};
			const options = {
				physics: true,
				edges: { arrows: { to: { enabled: false } } },
				nodes: { shape: "dot", size: 20 },
			};

			network = new vis.Network(container, data, options);

			nodes.forEach((nodeName) => {
				const srcOption = document.createElement("option");
				srcOption.value = nodeName;
				srcOption.textContent = nodeName;
				srcSelect.appendChild(srcOption);

				const dstOption = document.createElement("option");
				dstOption.value = nodeName;
				dstOption.textContent = nodeName;
				dstSelect.appendChild(dstOption);
			});
		})
		.catch((error) => {
			setError(error.message || "Failed to load data");
		});

	runButton.addEventListener("click", async () => {
		const src = srcSelect.value;
		const dst = dstSelect.value;
		setError("");

		if (!src || !dst) {
			setError("Select both source and destination nodes.");
			return;
		}

		runButton.disabled = true;
		runButton.textContent = "Finding...";

		try {
			const response = await fetch(
				`${API_BASE}/shortest-path?src=${encodeURIComponent(src)}&dst=${encodeURIComponent(dst)}`
			);
			const data = await response.json();
			if (!response.ok) {
				throw new Error(data.error || "Failed to fetch shortest path");
			}

			const dResult = data.dijkstra;

			const dEdges = new Set();

			for (let i = 0; i < dResult.path.length - 1; i += 1) {
				const edgeId = findEdgeId(dResult.path[i], dResult.path[i + 1]);
				if (edgeId !== null) {
					dEdges.add(edgeId);
				}
			}

			edgesDataSet.get().forEach((edge) => {
				const inD = dEdges.has(edge.id);

				if (inD) {
					edgesDataSet.update({
						id: edge.id,
						color: { color: "#1E90FF", highlight: "#1E90FF" },
						width: 4,
						dashes: false,
						shadow: { enabled: false },
					});
					return;
				}

				edgesDataSet.update({
					id: edge.id,
					color: { color: "#848484", highlight: "#848484" },
					width: 1,
					dashes: false,
					shadow: { enabled: false },
				});
			});

			document.getElementById("dijkstra-path").textContent = dResult.path.join(" → ");
			document.getElementById("dijkstra-distance").textContent = `${dResult.distance} km`;
			document.getElementById("dijkstra-steps").textContent = `${dResult.steps} relaxations`;

			updateComparison(dResult);
		} catch (error) {
			setError(error.message || "Failed to compute shortest path");
		} finally {
			runButton.disabled = false;
			runButton.textContent = "Find Shortest Path";
		}
	});
});
