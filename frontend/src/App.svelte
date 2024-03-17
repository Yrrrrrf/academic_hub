<script>
	import Query from "./components/Query.svelte";
	import AppHeader from "./components/AppHeader.svelte";

	export let name = 'Ñemña';


	let tables = [
		// "loan",
		// "user",
		// "publisher",
		// "author",
		// "topic",
		"library",
		"book",
	];

</script>

<main>
	<AppHeader name={name} />

	{#each tables as table}
		<Query
			table_name={table}
		/>
	{/each}

</main>


<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>
