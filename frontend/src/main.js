import App from './App.svelte';

const app = new App({
	target: document.body,
	props: {
		name: 'Library Inventory'
	}
});

export default app;