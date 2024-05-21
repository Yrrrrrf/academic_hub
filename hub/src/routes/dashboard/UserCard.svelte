<script>
    import { onMount } from 'svelte';
    import { api_url , user_type } from '../../stores.js';
    import { Avatar } from "@skeletonlabs/skeleton";

    export let token;

    let userData = null;
    let errorMessage = '';
    let apiUrl;
    let userType;

    $: user_type.subscribe(value => userType = value);
    $: api_url.subscribe(value => apiUrl = value);


    onMount(async () => {
        try {
            const response = await fetch(`${apiUrl}/users/me`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.ok) {
                userData = await response.json();
            } else {
                errorMessage = 'Failed to fetch user data';
                console.error('Fetch error:', response.statusText);
            }
        } catch (error) {
            errorMessage = 'An error occurred';
            console.error('Error:', error);
        }
    });
</script>

{#if errorMessage}
    <div class="mt-4 text-red-500 text-sm">{errorMessage}</div>
{:else if userData}
    <div class="max-w-md mx-auto shadow-md">
        <div class="flex items-center rounded-t-2xl p-4 variant-filled-surface">
            <Avatar background="bg-tertiary-500" border="border-4 border-surface-300-600-token hover:!border-primary-500" cursor="cursor-pointer">
                <span class="text-2xl font-bold leading-10 tracking-tight uppercase">{userData.name.charAt(0)}</span>
            </Avatar>
            <div class="flex-1 text-center">
                <h2 class="text-2xl font-bold mb-2">{userData.name}</h2>
                <p class="text-lg text-gray-400">{userData.email}</p>
            </div>
        </div>
        <h3 class="bg-gray-300 pt-6 pl-6 text-xl text-black">Logged In as: {userType.toUpperCase()}</h3>
        <div class="bg-gray-300 rounded-b-2xl p-6">
            <h3 class="text-xl text-black font-semibold">Additional Info</h3>
            {#if userData.additional_info && Object.keys(userData.additional_info).length > 0}
                <p class="text-black">{JSON.stringify(userData.additional_info)}</p>
            {:else}
                <p class="text-black">No additional data available...</p>
            {/if}
        </div>
    </div>
{:else}
    <div class="mt-4 text-gray-500 text-sm">Loading...</div>
{/if}
