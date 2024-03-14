<script>
	export let name;
	import AppHeader from "./components/AppHeader.svelte";
	import STable from "./components/STable.svelte";

</script>

<main>
<!--	<h1>Holis {name}!</h1>-->
	<AppHeader name="Library Management" />

	<STable />

</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>