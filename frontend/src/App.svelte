<script>
	import Query from "./components/Query.svelte";
	import AppHeader from "./components/AppHeader.svelte";

	export let name = 'Ñemña';


	let tables = [
		// {name: "user"},
		// {name: "publisher"},
		// {name: "author"},
		// {name: "topic"},
		// {name: "library"},
		{
			name: "book",
			qButtons: {
				"Pub": "/publisher_id=2",
				"ISBN": "/isbn={}",
			}
		},

		{
			name: "loan",
			qButtons: {
				book_serial_id: "/book_serial_id={}",
				return_date: "/return_date={}",
				loan_date: "/loan_date={}",
			}
		},

	];
</script>

<main>
	<AppHeader name={name} />

	{#each tables as table}
		<Query
			table_name={table.name}
			new_q_buttons={table.qButtons}
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
