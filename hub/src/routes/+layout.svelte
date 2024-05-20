<script lang="ts">
	import '../app.postcss';

	import { api_url} from "../stores";

	let apiUrl = '';
	$: api_url.subscribe(value => apiUrl = value);


	import { AppShell, AppBar } from '@skeletonlabs/skeleton';
	import { LightSwitch } from '@skeletonlabs/skeleton';

	import { browser } from '$app/environment';

	let app_name = 'Academic Hub';

	if (browser) {
		localStorage.setItem('api_url', api_url);
	}

	// import { initializeStores, Modal } from '@skeletonlabs/skeleton';
	//
	// initializeStores();

	// // Highlight JS
	// import hljs from 'highlight.js/lib/core';
	// import 'highlight.js/styles/github-dark.css';
	// import { storeHighlightJs } from '@skeletonlabs/skeleton';
	// import xml from 'highlight.js/lib/languages/xml'; // for HTML
	// import css from 'highlight.js/lib/languages/css';
	// import javascript from 'highlight.js/lib/languages/javascript';
	// import typescript from 'highlight.js/lib/languages/typescript';

	// hljs.registerLanguage('xml', xml); // for HTML
	// hljs.registerLanguage('css', css);
	// hljs.registerLanguage('javascript', javascript);
	// hljs.registerLanguage('typescript', typescript);
	// storeHighlightJs.set(hljs);

	// // Floating UI for Popups
	// import { computePosition, autoUpdate, flip, shift, offset, arrow } from '@floating-ui/dom';
	// import { storePopup } from '@skeletonlabs/skeleton';
	// storePopup.set({ computePosition, autoUpdate, flip, shift, offset, arrow });
</script>

<!--<Modal />-->

<svelte:head>
	<title>Academic Hub</title>
	<link rel="icon" type="image/png" href="/img/favicon.png" />
</svelte:head>



<!-- App Shell -->
<AppShell>
	<svelte:fragment slot="header">
		<!-- App Bar -->
		<AppBar>
			<svelte:fragment slot="lead">
				<strong class="text-xl uppercase">Welcome</strong>
			</svelte:fragment>

			<svelte:fragment slot="trail">
				<LightSwitch />
				<a
					class="btn btn-sm variant-ghost-primary"
					href="{apiUrl}/docs"
					target="_blank"
					rel="noreferrer"
				>API Docs</a>
				<a
					class="btn btn-sm variant-ghost-surface"
					href="https://github.com/Yrrrrrf/academic_hub"
					target="_blank"
					rel="noreferrer"
				>GitHub</a>
			</svelte:fragment>

		</AppBar>
	</svelte:fragment>

	<slot />  <!-- Page Route Content -->

	<!-- Some Footer Content -->
	<svelte:fragment slot="footer">
		<div class="variant-soft-tertiary"><h1>API URL: {apiUrl}</h1></div>
<!--		<p>This is some footer...<code class="code">/src/routes/+page.svelte</code></p>-->
	</svelte:fragment>

</AppShell>
