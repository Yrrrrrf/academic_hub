<script>
    import { onMount } from 'svelte';

    export let table_name;  // Mandatory prop (name of the table)
    export let new_q_buttons = {};  // Optional prop for additional query buttons

    let attr = ''; // Define a reactive attribute if needed
    let q_data = {
        'All': 's',
        'byId': '/id={}',
        'byName': '/name={}',
        ...new_q_buttons
    };  // Main query buttons (operations for the table)

    let columns = [];  // Define a reactive array if needed
    let rows = [];  // Define a reactive array if needed


    async function fetch_data(action = 'columns') {
        let url = `http://localhost:8000/${table_name}${action === 'columns' ? 's/dt/' : attr || ''}`;

        try {
            const data = await (await fetch(url)).json();
            console.log(data);
            action === 'columns' ? columns = data : rows = data;
        } catch (error) {console.error(`Error fetching ${action}:`, error)}
    }

    onMount(() => {
        fetch_data();  // Fetch columns
        console.log(q_data);  // Log the query buttons for debugging
    });

    // Function to handle button clicks
    function handleButtonClick(action) {
        attr = q_data[action];
        fetch_data('rows');  // Fetch rows
    }


</script>


<div class="query-container">
    <h1>{table_name.charAt(0).toUpperCase() + table_name.slice(1)}</h1>
    {#each Object.keys(q_data) as action}
        <button on:click={() => handleButtonClick(action)}>
            {action}
        </button>
    {/each}
</div>

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
