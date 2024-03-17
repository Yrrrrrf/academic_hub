<!-- QueryItem.svelte -->
<script>
    export let imageUrl = ''; // URL to the image
    export let name = ''; // Name of the item
    export let id = ''; // ID of the item
    export let additionalData = {}; // Object with the rest of the data

    // Placeholder image or icon URL
    const placeholderImage = 'placeholder-icon-url-here'; // Update this with your desired placeholder
</script>

<div class="query-item">
    <div class="media">
        <img alt="Item image"
             class="image"
             on:error={
                () => (imageUrl = placeholderImage)
                } src={imageUrl || placeholderImage}
        />
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
        align-items: flex-start; /* Adjust alignment */
        gap: 20px;
        background-color: #f9f9f9; /* Lighter background */
        border-radius: 16px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15); /* Softer shadow */
        padding: 20px;
        margin: 20px;
        transition: transform 0.2s; /* Smooth transition */
    }

    .query-item:hover {
        transform: translateY(-5px); /* Slight lift on hover */
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2); /* Enhanced shadow on hover */
    }

    .media {
        flex-shrink: 0;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .image {
        width: 100px; /* Adjust as needed */
        height: 100px; /* Adjust as needed */
        object-fit: cover;
        border-radius: 50%; /* Circular image */
        border: 2px solid #eaeaea; /* Image border for distinction */
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
        font-weight: 600; /* Slightly less bold */
        color: #333; /* Darker font color */
    }

    .id {
        font-size: 16px;
        color: #666; /* Lighter font color */
        margin-top: 5px;
    }

    .additional-data {
        margin-top: 15px;
        padding-top: 10px;
        border-top: 1px solid #eee; /* Separator */
    }

    .data-field {
        margin-bottom: 5px;
    }

    .data-field strong {
        margin-right: 5px;
        color: #444; /* Strong color for key */
    }
</style>
