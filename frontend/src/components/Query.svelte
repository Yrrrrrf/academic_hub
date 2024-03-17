<script>
    import { onMount } from 'svelte';
    import SItemCard from "./SItemCard.svelte";

    export let table_name;  // Mandatory prop (name of the table)
    export let new_q_buttons = {};  // Optional prop for additional query buttons

    let attr = ''; // Define a reactive attribute if needed
    let q_data = {
        'All': 's',
        'ID': '/id={id}',
        'NAME': '/name={name}',
        ...new_q_buttons
    };  // Main query buttons (operations for the table)

    let columns = [];  // Define a reactive array if needed
    let rows = [];  // Define a reactive array if needed


    // ? temp
    let idInput = '';
    let nameInput = '';

    // async function fetch_data(action = 'columns') {
    //     let url = `http://localhost:8000/${table_name}${action === 'columns' ? 's/dt/' : attr}`;

    // modified fetch_data function to always recibe always the action
    async function fetch_data(action) {
        try {
            const response = await fetch(`http://localhost:8000/${table_name}${action}`);
            if (!response.ok) new Error('Server responded with an error.');
            const data = await response.json();
            // return the data to the caller
            return Array.isArray(data) ? data : [data];   // Always convert to array
            // rows = Array.isArray(data) ? data : [data];   // Always convert to array
        }
        catch (error) {
            console.error(`Error fetching ${action}:`, error);
            rows = []; // Clear rows on error: t
        }
    }

    async function get_columns() {
        columns = await fetch_data('s/dt/');
        console.log(columns);
    }

    onMount(() => {
        get_columns();
    });

    // function handleButtonClick() {
    //     let data = fetch_data('s').then(data => {
    //         console.log(data);
    //         let item = data;
    //     });
    // }



    let selectedItem = null;

    async function handleButtonClick(column) {
        let action;
        switch (column) {
            default:
                action = `/${column.toLowerCase()}=1}`;
                console.log(action);
                break;
        }

        rows = await fetch_data(action);
        if (rows.length > 0) {
            // Assuming the first element is the selected one
            selectedItem = {
                imageUrl: rows[0].imageUrl || 'default_image.jpg', // Replace with actual image field
                name: rows[0].name || '', // Replace with actual name field
                id: rows[0].id || '', // Replace with actual id field
                additionalData: { ...rows[0] }
            };
        }
    }



</script>


<main>

    <div class="query-container">
        <h1>{table_name.charAt(0).toUpperCase() + table_name.slice(1)}</h1>
    </div>

    <button on:click={() => handleButtonClick()}>All</button>  <!-- Default query button (all rows) -->
    {#each columns as column}
        <!-- Individual query buttons (operations for the table) -->
        <button on:click={() => handleButtonClick(column)}>{column}</button>
    {/each}

    {#if selectedItem}
        <SItemCard
                imageUrl={selectedItem.imageUrl}
                name={selectedItem.name}
                id={selectedItem.id}
                additionalData={selectedItem.additionalData}
        />
    {/if}

</main>

<style>
    .query-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 10px;
        background-color: #FFF3E0;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        max-width: 300px;
        margin: auto;
    }

    button {
        background-color: #FB8C00;
        color: white;
        padding: 10px 15px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }

    button:hover {
        background-color: #FFA726;
    }
</style>
