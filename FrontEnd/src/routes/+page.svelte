<script>
	import hello from '$lib/images/Hello-PNG-Image.png';
</script>

<svelte:head>
	<title>Home</title>
	<meta name="description" content="Svelte demo app" />
</svelte:head>

<section>
	<div class="slide-content">
		<img src={hello} alt="Hello" style="width: 500px; padding-top: 20px;" />
		<h1>This is my project! To get started, navigate to the tab at the top labeled "graph."</h1>
	</div>
</section>

<style>
	section {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		flex: 0.6;
	}

	.slide-content {
		margin: 0 auto;
		width: 100%;
		line-height: 1.1;
		margin-top: -30px;
		font-weight: 400;
		margin-bottom: 30px;
		width: 75%;
		text-align: center;
		padding: 20px;
	}

	h1 {
		color: #333; /* Adjust text color as needed */
		font-size: 24px; /* Adjust font size as needed */
		margin-top: 20px;
	}
</style>
