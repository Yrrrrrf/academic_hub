<script>
    import { goto } from '$app/navigation'; // Correct import
    export let name = 'Academic Hub';
    let email = '';
    let password = '';
    let errorMessage = '';
    let successMessage = '';

    async function handleSubmit(event) {
        event.preventDefault();
        errorMessage = '';
        successMessage = '';

        const formData = new URLSearchParams();
        formData.append('username', email);
        formData.append('password', password);

        const response = await fetch('http://127.0.0.1:8000/login_token', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: formData
        });

        if (response.ok) {
            const data = await response.json();
            successMessage = 'Login successful!';
            console.log('Login successful:', data);
            // Redirect or show the next component
            // After successful login
            // data is a dictionary with the token
            // selected the 'access_token' key
            localStorage.setItem('access_token', data.access_token);



            goto('/dashboard'); // Example redirect to dashboard
        } else {
            errorMessage = 'Login failed: ' + response.statusText;
            console.error('Login failed:', response.statusText);
        }
    }
</script>

<div class="max-w-md relative flex flex-col p-4 rounded-md text-black bg-white">
    <div class="text-2xl font-bold mb-2 text-[#1e0e4b] text-center">Welcome back to <span
            class="text-[#7747ff]">{name}</span></div>
    <div class="text-sm font-normal mb-4 text-center text-[#1e0e4b]">Log in to your account</div>
    <form class="flex flex-col gap-3" on:submit={handleSubmit}>
        <div class="block relative">
            <label for="email"
                   class="block text-gray-600 cursor-text text-sm leading-[140%] font-normal mb-2">Email</label>
            <input type="email" id="email" bind:value={email}
                   class="rounded border border-gray-200 text-sm w-full font-normal leading-[18px] text-black tracking-[0px] appearance-none block h-11 m-0 p-[11px] focus:ring-2 ring-offset-2 ring-gray-900 outline-0">
        </div>
        <div class="block relative">
            <label for="password" class="block text-gray-600 cursor-text text-sm leading-[140%] font-normal mb-2">Password</label>
            <input type="password" id="password" bind:value={password}
                   class="rounded border border-gray-200 text-sm w-full font-normal leading-[18px] text-black tracking-[0px] appearance-none block h-11 m-0 p-[11px] focus:ring-2 ring-offset-2 ring-gray-900 outline-0">
        </div>
        <div>
            <a class="text-sm text-[#7747ff]" href="#">Forgot your password?</a>
        </div>
        <button type="submit" class="bg-[#7747ff] w-max m-auto px-6 py-2 rounded text-white text-sm font-normal">
            Submit
        </button>
    </form>
    {#if errorMessage}
        <div class="mt-4 text-red-500 text-sm">{errorMessage}</div>
    {/if}
    {#if successMessage}
        <div class="mt-4 text-green-500 text-sm">{successMessage}</div>
    {/if}
</div>
