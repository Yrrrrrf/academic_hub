<script>
	import { page } from '$app/stores';
	import logo from '$lib/images/diary.png';
	import github from '$lib/images/github.svg';
	export let name = 'Academic Hub';

</script>

<!--OLD HEADER-->
<!--<header>-->
<!--	<div class="corner">-->
		<a href="/"><img src={logo} alt="Academic Hub Logo" /></a>
<!--	</div>-->

<!--	<nav>-->
<!--		<ul>-->
<!--			{#each pages as { path, label }}-->
<!--				<li aria-current={$page.url.pathname === path ? 'page' : undefined}>-->
<!--					<a href={path}>{label}</a>-->
<!--				</li>-->
<!--			{/each}-->
<!--		</ul>-->
<!--	</nav>-->
<!--	<div class="corner">-->
<!--		<a href="https://github.com/Yrrrrrf/academic_hub" target="_blank" rel="noopener">-->
<!--			<img src={github} alt="GitHub" />-->
<!--		</a>-->
<!--	</div>-->
<!--</header>-->

<header class="flex justify-between items-center p-4 bg-white shadow-md">
	<div class="text-2xl font-bold text-[#1e0e4b]">
		Welcome to {name}
	</div>
	<nav class="flex gap-4">
		<a href="/ssss" class="text-blue-500 hover:text-blue-700">Home</a>
		<a href="/" class="text-blue-500 hover:text-blue-700">About</a>
		<a href="https://github.com/Yrrrrrf/academic_hub" target="_blank" class="text-blue-500 hover:text-blue-700">Repository</a>
		<a href="/" class="text-blue-500 hover:text-blue-700">Login</a>
		<a href="/" class="text-blue-500 hover:text-blue-700">Some Other Useful Button</a>
	</nav>
</header>

<style>
	header {
		background-color: #ffffff;
		box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
	}
	nav a {
		text-decoration: none;
		font-size: 1rem;
	}
</style>
