<script lang="ts">
	import SpecialButton from '../SpecialButton.svelte';
	import LoginForm from '../LoginForm.svelte';
	import SignUpForm from '../SignUpForm.svelte';

	export let app_name = 'Academic Hub';

	let showSignUp: boolean = false;
	let showLogIn: boolean = false;

	function closeModal() {
		showLogIn = false;
		showSignUp = false;
	}
</script>

<main class="container h-full mx-auto flex justify-center items-center">
	<div class="space-y-10 text-center flex flex-col items-center variant-filled-surface p-8 rounded-lg z-10">
		<h2 class="h2">Welcome to {app_name}</h2>
		<SpecialButton text="Log In" onClick={() => showLogIn = true} />
		<SpecialButton text="Sign Up" onClick={() => showSignUp = true} />
	</div>

	{#if showLogIn}<LoginForm {closeModal} />{/if}
	{#if showSignUp}<SignUpForm {closeModal} />{/if}
</main>

<style>
	.container {
		background-size: cover;
		background-position: center;
	}
</style>
