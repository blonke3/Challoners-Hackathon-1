<svelte:head>
	<title>How to use this tool</title>
	<meta name="description" content="How to use this tool" />
</svelte:head>

<div class="text-column">
	<h1>How to use this circuit solving tool</h1>

	<p>
		Choose what type of node you are going to create from the menu at the top. You are allowed only one source and sink node
		(for simplicity) but you can have as many unknown nodes as you'd like.
	</p>
	<p>
		You can then draw connections (or edges) between these nodes which will represent the wires in this circuit.
	</p>
	<p>
		For simplicity, we will assume a unit voltage into the circuit. If you want to consider other voltages then you simply
		have to multiply all other values by this factor change.
	</p>
	<p>
		To solve the circuit (i.e. work out the rest of the voltages / currents) you can click the solve button at the bottom.
	</p>

	<p>
		For now, this circuit will assume unit resistance between nodes. This may change...
	</p>
</div>

<style>
</style>
