<script>
    import BaseForm from './BaseForm.svelte';
    import { api_url, access_token, user_type } from './stores.js';
    import { goto } from '$app/navigation';
    import { RadioGroup, RadioItem } from '@skeletonlabs/skeleton';
    import { writable } from 'svelte/store';

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

    // Import user_type store
    let userType = '';
    let someMessage = '';

    const userTypes = ['student', 'teacher', 'admin'];

    function currentType() {
        console.log('Current type:', userType);
        user_type.set(userType);
    }

</script>

<BaseForm title="Log In" onSubmit={handleSubmit} {closeModal}>
    <div slot="user-type-selector" class="flex flex-col items-center mt-4">
        <RadioGroup bind:group={userType} class="flex space-x-4">
            {#each userTypes as type}
                <RadioItem bind:group={userType} name={type} value={type.charAt(0).toUpperCase() + type.slice(1)} on:change={currentType}>
                    {type.charAt(0).toUpperCase() + type.slice(1)}
                </RadioItem>
            {/each}
        </RadioGroup>
    </div>
    <div slot="message">
        {#if someMessage}
            <div class="flex justify-center text-red-500">{someMessage}</div>
        {/if}
    </div>
</BaseForm>

<style>
    .inset-0 {
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
    }
</style>
