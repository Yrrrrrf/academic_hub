<script>
	import { browser } from '$app/environment';
	import NeoForm from './NeoForm.svelte';

	let showForm = false;

	export let name = 'Academic Hub';

	function toggleForm() {
		showForm = !showForm;
	}


	if (browser) {
		localStorage.clear();
		// todo: Check how to set a default token (for testing)
		// const defaultToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdHJpbmciLCJpZCI6MjIsImV4cCI6MTcxNjE3NjA0NX0._kv9MhapQVDBoihHzzbZt1maguXuc-56SUfJVtwN-Lg';
		// localStorage.setItem('access_token', defaultToken);
	}

</script>

<svelte:head><title>{name}</title></svelte:head>

<main>
	<h1>Welcome to Academic Hub</h1>

	<button on:click={toggleForm}>Login</button>
	{#if showForm}
		<NeoForm {name}/>
	{/if}


</main>

<style>
	main {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		flex: 0.6;
		background-image: url('$lib/img/some_campus.png'); /* Add the path to your background image */
		background-size: cover;
		background-position: center;
		height: 100vh;
		color: white;
	}

	h1 {
		width: 100%;
		font-size: 3rem;
		text-align: center;
		margin: 0;
	}

	button {
		margin-top: 1rem;
		padding: 0.5rem 1rem;
		font-size: 1rem;
		cursor: pointer;
	}

</style>
