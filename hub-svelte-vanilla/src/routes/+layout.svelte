<script>
	import Header from './Header.svelte';
	import './../app.css';
</script>

<main>
	<Header />
	<slot />  <!-- Here we render the content of the page (+page.svelte) -->

<!--	<footer class="flex flex-col justify-center items-center p-3">-->
<!--		<p class="text-center">Check <a href="http://github.com/Yrrrrrf/academic_hub" target="_blank" class="text-blue-500">source code</a> on GitHub</p>-->
<!--	</footer>-->
</main>


<style>
	@media (min-width: 480px) {
		footer {
			padding: 12px 0;
			}
	}
</style>
