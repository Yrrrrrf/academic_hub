<script>
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation'; // For redirection if needed

    let userData = null;
    let errorMessage = '';

    onMount(async () => {
        try {
            const token = localStorage.getItem('access_token');
            if (!token) {
                errorMessage = 'No token found. Please log in.';
                goto('/login'); // Redirect to login if no token found
                return;
            }

            const response = await fetch('http://127.0.0.1:8000/users/me', {
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
                // Optionally redirect to login if not authenticated
                // goto('/login');
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
    <div class="max-w-md mx-auto p-4 rounded-md text-black bg-white shadow-md">
        <h2 class="text-2xl font-bold mb-4 text-center text-[#1e0e4b]">User Information</h2>
        <div class="text-center">
            <p class="text-lg"><strong>Name:</strong> {userData.name}</p>
            <p class="text-lg"><strong>Email:</strong> {userData.email}</p>
            <p class="text-lg"><strong>Additional Info:</strong> {JSON.stringify(userData.additional_info)}</p>
        </div>
    </div>
{:else}
    <div class="mt-4 text-gray-500 text-sm">Loading...</div>
{/if}
