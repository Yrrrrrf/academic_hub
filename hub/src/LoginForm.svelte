<script>
    import BaseForm from './BaseForm.svelte';
    import { api_url, access_token } from './stores.js';
    import { goto } from '$app/navigation';

    let apiUrl = '';
    $: api_url.subscribe(value => apiUrl = value);

    export let closeModal;

    async function handleSubmit({ email, password }) {
        const formData = new URLSearchParams();
        formData.append('username', email);
        formData.append('password', password);

        const request_url = `${apiUrl}/login_token`;
        console.log('Request URL:', request_url);

        const response = await fetch(request_url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: formData
        });

        if (response.ok) {
            const data = await response.json();
            console.log('Login successful:', data);
            access_token.set(data.access_token);
            goto('/dashboard');
        } else {
            console.error('Login failed:', response.statusText);
        }
    }
</script>

<BaseForm title="Log In" onSubmit={handleSubmit} {closeModal} />
