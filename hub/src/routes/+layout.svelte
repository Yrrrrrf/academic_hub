<script>
	import Header from './Header.svelte';
	import './../app.css';
</script>

<div class="app">
	<Header />

	<main>
		<slot />
	</main>


	<f4ooter class="flex flex-col justify-center items-center p-3">
		<p>Check <a href="http://github.com/Yrrrrrf/academic_hub/tree/main/hub" target="_blank">source code</a> on GitHub</p>
	</f4ooter>


</div>

<style>
	.app {
		display: flex;
		flex-direction: column;
		min-height: 100vh;
	}

	main {
		flex: 1;
		display: flex;
		flex-direction: column;
		padding: 1rem;
		width: 100%;
		max-width: 64rem;
		margin: 0 auto;
		box-sizing: border-box;
	}

	@media (min-width: 480px) {
		footer {
			padding: 12px 0;
		}
	}
</style>
