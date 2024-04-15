<script>
	import CircuitNode from "./CircuitNode.svelte";
	
	let nodes = []; // Initialize nodes array
	let edges = []; // Initialize edges array
	let current1 = ""; // Initialize current for Node 1
	let nodesCreated = false; // Track whether nodes 1 and 2 have been created
	let selectedNodeId = 0;
	let addingEdge = false;
	let enabledConductance = false;
	
	// Function to initialize nodes with provided currents
	function initializeNodes() {
		current1 = Number(current1)
		let valid = !isNaN(current1) && Number.isFinite(current1)
		if (valid) {
			nodes = [
			{ id: 1, voltage: "x", current: current1, x: 250, y: 300 },
			{ id: 2, voltage: 0, current: -current1, x: 250, y: 450 }
		];
		nodesCreated = true; // Set nodesCreated to true once nodes 1 and 2 are created
		} else {
			alert("That doesn't seem to be a finite number!")
		}
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

	function clearCircuit() {
		nodes = [];
		edges = [];
		nodesCreated = false;
		addingEdge = false;
		current1 = "";
		selectedNodeId = 0;
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
			let conductance_value = 1
			if (enabledConductance === true) {
				let valid = false;
				while (!valid) {
					conductance_value = Number(prompt("Enter the value of conductance:"));
					valid = !isNaN(conductance_value) && Number.isFinite(conductance_value);
					if (!valid) {
						alert("That was not a number!")
					}
				}
			}
			edges = [...edges, { source: selectedNodeId, target: nodeId, conductance: conductance_value }];
			console.log("Connected Nodes:", selectedNodeId, nodeId);
			selectedNodeId = 0; // Reset selected node
			addingEdge = false;
			}
		}
	}

	function update_voltages(voltages) {
		for (let index=0; index < nodes.length; index++) {
			if (index < voltages.length) {
				nodes[index]["voltage"] = voltages[index].toFixed(2)
			} else {
				nodes[index]["voltage"] = 0
			}				
		}
	}

	function POST_data() {
		const backendUrl = "http://127.0.0.1:5000";


		fetch(backendUrl + "/process_data/", {
			method: "POST",
			headers: {
				"Content-Type": "application/json"
			},
			body: JSON.stringify({ edges, current1 })
		})
		.then(response => {
			if (response.ok) {
				console.log("data sent to backend successfully");
				return response.json();
			} else {
				console.error("Failed to send data to backend");
			}
		})
		.then(returned_data => {
			console.log(returned_data);
			if (returned_data && returned_data.length > 0) {
				update_voltages(returned_data)
			} else {
				alert("Nodes 1 and 2 must be connected for this program to work. This is because they are the source and sink nodes so them not being connected means the current can't flow which we are assuming it does!")
			}
		})
		.catch(error => {
			console.error("Error sending data to backend:", error);
		});
	}

	function solveCircuit() {
		POST_data()
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
			<div class="checkbox-container">
				<input type="checkbox" bind:checked={enabledConductance} id="enableConductance">
				<label for="enableConductance">Enable Conductance Input (default: 1)</label>    	
			</div>
			<button class="draw-edge-button" on:click={addEdge}>Draw Edge</button>
			<button class="solve-graph" on:click={solveCircuit}>Solve Circuit to find Voltages</button>
			<button class="clear-graph" on:click={clearCircuit}>Clear the circuit</button>
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
							<text
								x={(node.x + node2.x + 100) / 2}
								y={(node.y + node2.y + 100) / 2}
								font-size="12"
								text-anchor="middle"
								alignment-baseline="middle"
								style="fill: red; font-weight: bold; font-size: 14px;"
                        	>
                            {edge.conductance}
                        	</text>
						{/if}
					{/each}
				{/if}
			{/each}
		{/each}
	</svg>
	
</main>


<style>
	.checkbox-container {
		position: absolute;
        display: flex;
        align-items: center;
		top: calc(10rem + 20px);
		left: 30vw;
    }

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

	.clear-graph {
		position: absolute;
		top: calc(14rem + 20px);
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