<script>
    import { api_url, access_token } from './stores.js';
    import {goto} from "$app/navigation";

    let apiUrl = '';

    $: api_url.subscribe(value => apiUrl = value);

    let email = '';
    let password = '';
    let someMessage = '';

    export let closeModal;

    async function handleSubmit(event) {
        event.preventDefault();

        const formData = new URLSearchParams();
        formData.append('username', email);
        formData.append('password', password);

        let request_url = `${apiUrl}/login_token`;
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
            access_token.set(data.access_token); // Set the token in the store
            closeModal();


            goto('/dashboard')
        } else {
            someMessage = 'Login failed: ' + response.statusText;
            console.error('Login failed:', response.statusText);
        }
    }

    function handleOverlayClick(event) {
        if (event.target === event.currentTarget) {
            closeModal();
        }
    }
</script>


<div class="fixed inset-0 bg-black bg-opacity-60 flex justify-center items-center z-50" on:click={handleOverlayClick}>
    <div class="variant-glass-surface p-10 rounded-lg shadow-lg z-50 max-w-md w-full">
        <strong class="h3 uppercase flex justify-center">Log In</strong>
        <form on:submit={handleSubmit} class="flex flex-col space-y-4">
            <div class="form-group">
                <label for="email" class="h4 font-medium">Email</label>
                <input type="email" id="email" bind:value={email} class="variant-soft-tertiary w-full p-2 rounded-md" required/>
            </div>
            <div class="form-group">
                <label for="password" class="h4 font-medium">Password</label>
                <input type="password" id="password" bind:value={password} class="variant-soft-tertiary w-full p-2 rounded-md" required/>
            </div>
            <button type="submit" class="btn variant-filled-primary">Log In</button>
            {#if someMessage}
                <div class="flex justify-center text-red-500">{someMessage}</div>
            {/if}
        </form>
    </div>
</div>

<style>
    .inset-0 {
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
    }
</style>
