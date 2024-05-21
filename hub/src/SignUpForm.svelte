<script>
    import { api_url, access_token } from './stores.js';
    import { goto } from "$app/navigation";
    import BaseForm from './BaseForm.svelte';

    let apiUrl = '';
    $: api_url.subscribe(value => apiUrl = value);

    export let closeModal;

    let name = '';
    let email = '';
    let password = '';
    let confirmPassword = '';
    let someMessage = '';

    async function handleSubmit(formData) {
        const { name, email, password, confirmPassword } = formData;

        if (password !== confirmPassword) {
            someMessage = "Passwords do not match!";
            return;
        }

        const body = {
            name,
            email,
            password,
            additional_info: {}
        };

        console.log('Request Body:', body);

        const response = await fetch(`${apiUrl}/general_user`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${access_token}`
            },
            body: JSON.stringify(body)
        });

        if (response.ok) {
            const result = await response.json();
            // handle successful registration (e.g., redirect, show message, etc.)
        } else {
            const error = await response.json();
            someMessage = error.message || 'Registration failed!';
        }
    }
</script>

<BaseForm title="Sign Up" onSubmit={handleSubmit} {closeModal} bind:name={name} bind:confirmPassword={confirmPassword}>
    <div slot="name" class="form-group">
        <label for="name" class="h4 font-medium">Name</label>
        <input type="text" id="name" bind:value={name} class="variant-soft-tertiary w-full p-2 rounded-md" required/>
    </div>
    <div slot="confirm-password" class="form-group">
        <label for="confirm-password" class="h4 font-medium">Confirm Password</label>
        <input type="password" id="confirm-password" bind:value={confirmPassword} class="variant-soft-tertiary w-full p-2 rounded-md" required/>
    </div>
    <div slot="message" class="flex justify-center text-red-500">{someMessage}</div>
</BaseForm>
