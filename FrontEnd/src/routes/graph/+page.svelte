<script>
	import { onMount } from "svelte";
	import CircuitNode from "./CircuitNode.svelte";
	
	let nodes = []; // Initialize nodes array
	let edges = []; // Initialize edges array
	let current1 = ""; // Initialize current for Node 1
	let nodesCreated = false; // Track whether nodes 1 and 2 have been created
	let selectedNodeId = 0;
	let addingEdge = false;
	
	// Function to initialize nodes with provided currents
	function initializeNodes() {
		nodes = [
			{ id: 1, voltage: "x", current: current1, x: 250, y: 250 },
			{ id: 2, voltage: 0, current: -current1, x: 250, y: 400 }
		];
		nodesCreated = true; // Set nodesCreated to true once nodes 1 and 2 are created
	}
	
	// Function to add a new node with voltage set at "x" and current set to 0
	function addNode() {
		const newNodeId = nodes.length + 1;
		nodes = [...nodes, { id: newNodeId, voltage: "x", current: 0, x: 100, y: 100 }];
	}
	
	// Function to handle submit button click
	function handleSubmit() {
		initializeNodes(); // Confirm the currents and create nodes 1 and 2
	}

	function addEdge() {
		addingEdge = !addingEdge;
	}

	// Function to handle node click
	function handleNodeClick(event, nodeId) {
		const { x, y } = event.detail
		console.log(edges, nodeId, selectedNodeId, x, y, addingEdge);
		if (addingEdge === true) {
			if (selectedNodeId === 0 || selectedNodeId === nodeId) {
			// First node selected
			selectedNodeId = nodeId;
			} else {
			// Second node selected, draw edge
			edges = [...edges, { source: selectedNodeId, target: nodeId }];
			console.log("Connected Nodes:", selectedNodeId, nodeId);
			selectedNodeId = 0; // Reset selected node
			addingEdge = false;
			}
		}
	}

	function POST_edges() {
		const backendUrl = "http://127.0.0.1:5000/process_edges/";

		fetch(backendUrl, {
			method: "POST",
			headers: {
				"Content-Type": "application/json"
			},
			body: JSON.stringify({ edges, current1 })
		})
		.then(response => {
			if (response.ok) {
				console.log("Edges sent to backend successfully");
			} else {
				console.error("Failed to send edges to backend");
			}
		})
		.catch(error => {
			console.error("Error sending edges to backend:", error);
		});
	}

	function solveCircuit() {
		POST_edges()
	}

</script>

<main>
	<h2>
		Graphed Circuit Solver
	</h2>

	<a class="how-to-use" href="/graph/how-to-use">How to use</a>

	<div>
		{#if !nodesCreated}
			<input type="text" placeholder="Enter current for Node 1" bind:value={current1}>
			<button on:click={handleSubmit}>Submit</button>
		{/if}
		
		{#each nodes as node (node.id)}
			<CircuitNode bind:x={node.x} bind:y={node.y} on:nodeClick={(event) => handleNodeClick(event, node.id)}>
				<div slot="CircleText" let:voltage let:current>
					<h3> Node {node.id} </h3> Voltage: {node.voltage} <br> Current: {node.current}
				</div>
			</CircuitNode>
		{/each}
	</div>

	<!-- Button to add a new node (conditionally rendered) -->
	{#if nodesCreated}
		<button class="add-node-button" on:click={addNode}>Add Node</button>
		<button class="draw-edge-button" on:click={addEdge}>Draw Edge</button>
		<button class="solve-graph" on:click={solveCircuit}>Solve Circuit to find Voltages</button>
	{/if}

	<svg class="svg-container">
		{#each edges as edge}
			{#each nodes as node}
				{#if node.id === edge.source}
					{#each nodes as node2}
						{#if node2.id === edge.target}
							<line
								x1={node.x + 50}
								y1={node.y + 50}
								x2={node2.x + 50}
								y2={node2.y + 50}
								stroke="black"
								stroke-width="2"
								class="edge"
							/>
						{/if}
					{/each}
				{/if}
			{/each}
		{/each}
	</svg>
	
</main>


<style>
	.add-node-button {
		position: absolute;
		top: calc(8rem + 20px);
		left: 17.75vw;
	}	
	
	.draw-edge-button {
		position: absolute;
		top: calc(10rem + 20px);
		left: 17.75vw;
	}

	.solve-graph {
		position: absolute;
		top: calc(12rem + 20px);
		left: 17.75vw;
	}

	.edge {
		position: fixed;
		top: 0;
		left: 0;
		color: "red"
	}

	.svg-container {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		padding: 0;
		margin: 0;
		z-index: -999;
	}

	h2 {
		left: 18vw;
	}

	.how-to-use::before {
		content: "i";
		display: inline-block;
		font-size: 0.8em;
		font-weight: 900;
		width: 1em;
		height: 1em;
		padding: 0.2em;
		line-height: 1;
		border: 1.5px solid var(--color-text);
		border-radius: 50%;
		text-align: center;
		margin: 0 0.5em 0 0;
		position: relative;
		top: -0.05em;
		margin-bottom: 1vh;
	}
</style>