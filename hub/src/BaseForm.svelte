<script>
    export let title = '';
    export let onSubmit;
    export let closeModal;
    export let name = ''; // New prop for name
    export let confirmPassword = ''; // New prop for confirm password

    let email = '';
    let password = '';

    function handleSubmit(event) {
        event.preventDefault();
        const formData = { name, email, password, confirmPassword };
        onSubmit(formData);
    }

    function handleOverlayClick(event) {
        if (event.target === event.currentTarget) {
            closeModal();
        }
    }
</script>

<div class="fixed inset-0 bg-black bg-opacity-60 flex justify-center items-center z-50" on:click={handleOverlayClick}>
    <div class="variant-glass-surface p-10 rounded-lg shadow-lg z-50 max-w-md w-full">
        <strong class="h3 uppercase flex justify-center">{title}</strong>
        <slot name="user-type-selector"></slot>
        <form on:submit={handleSubmit} class="flex flex-col space-y-4">
            <slot name="name"></slot>
            <div class="form-group">
                <label for="email" class="h4 font-medium">Email</label>
                <input type="email" id="email" bind:value={email} class="variant-soft-tertiary w-full p-2 rounded-md" required/>
            </div>
            <div class="form-group">
                <label for="password" class="h4 font-medium">Password</label>
                <input type="password" id="password" bind:value={password} class="variant-soft-tertiary w-full p-2 rounded-md" required/>
            </div>
            <slot name="confirm-password"></slot>
            <p></p>
            <button type="submit" class="btn variant-filled-primary ">{title}</button>
            <slot name="message"></slot>
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
