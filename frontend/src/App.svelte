<script>
	// import Query from "./components/Query.svelte";

	import Query from "./components/Query.svelte";
	import AppHeader from "./components/AppHeader.svelte";

	export let name = 'Ñemña';
	import STable from "./components/STable.svelte";

	let table_names = [
			// "author",
			"book",
			// "loan",
			// "publisher",
			// "topic",
			// "user",
			// "libraries",
	];



</script>

<main>
	<AppHeader name = {name} />

	{#each table_names as table_name}
		<Query
			table_name={table_name}
			new_q_buttons={
				{
					"Pub": "/publisher_id={}",
					"ISBN": "/isbn={}",
				}
			}
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
