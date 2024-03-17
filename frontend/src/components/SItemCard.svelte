<!-- QueryItem.svelte -->
<script>
    export let imageUrl = 'https://via.placeholder.com/150'; // URL to the image
    export let name = ''; // Name of the item
    export let id = ''; // ID of the item
    export let additionalData = {}; // Object with the rest of the data

    // Determine if an image is provided
    $: hasImage = imageUrl !== '';
</script>

<div class="query-item">
    <div class="media">
        {#if hasImage}
            <img class="image" src={imageUrl} alt="Item image" />
        {:else}
            <div class="image placeholder">
                No Image Available
            </div>
        {/if}
    </div>
    <div class="details">
        <h2 class="name">{name}</h2>
        <p class="id">ID: {id}</p>
        <div class="additional-data">
            {#each Object.entries(additionalData) as [key, value]}
                <div class="data-field">
                    <strong>{key}:</strong> {value}
                </div>
            {/each}
        </div>
    </div>
</div>

<style>
    .query-item {
        display: flex;
        align-items: center;
        gap: 20px;
        background-color: #f9f9f9;
        border-radius: 16px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
        padding: 20px;
        margin: 20px;
        position: relative; /* Needed for text overlay */
    }

    .media {
        flex-shrink: 0;
        position: relative;
        width: 100px; /* Fixed size */
        height: 100px; /* Fixed size */
        border-radius: 50%; /* Circular shape */
        overflow: hidden; /* Ensure content fits */
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #eaeaea; /* Background for the placeholder */
    }

    .image {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    .placeholder {
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        color: #666;
        font-weight: bold;
    }

    .details {
        flex-grow: 1;
    }

    .name, .id {
        margin: 0;
        padding: 0;
    }

    .name {
        font-size: 24px;
        font-weight: bold;
        color: black; /* BLACK color for name */
    }

    .id {
        font-size: 16px;
        color: #666; /* Lighter for ID */
        margin-top: 5px;
    }

    .additional-data {
        margin-top: 15px;
        padding-top: 10px;
        border-top: 1px solid #eee;
    }

    .data-field {
        margin-bottom: 5px;
    }

    .data-field strong {
        margin-right: 5px;
        color: #444;
    }
</style>
