<script>
    import { onMount } from 'svelte';
    import SItemCard from "./SItemCard.svelte";

    export let table_name;  // Mandatory prop (name of the table)

    let columns = [];  // Define a reactive array if needed

    // async function fetch_data(action = 'columns') {
    //     let url = `http://localhost:8000/${table_name}${action === 'columns' ? 's/dt/' : attr}`;

    // modified fetch_data function to always recibe always the action
    async function fetch_data(action) {
        try {
            const response = await fetch(`http://localhost:8000/${table_name}${action}`);
            if (!response.ok) new Error('Server responded with an error.');
            const data = await response.json();
            return Array.isArray(data) ? data : [data];   // Always convert to array
        }
        catch (error) {console.error(`Error fetching ${action}:`, error);}
    }

    async function get_columns() {
        columns = await fetch_data('s/dt/');
        console.log(columns);
    }

    onMount(() => {
        get_columns();
    });

    let show_card = false;

    async function handleButtonClick(action) {
        // action = action.replace('{}', idInput);  // REPLACE {} WITH THE VALUE OF THE INPUT
        // fetch_data(action).then(data => console.log(data));
        let data = (await fetch_data(action));
        console.log(data);
    }

</script>


<main>

    <div class="query-container">
        <h1>{table_name.charAt(0).toUpperCase() + table_name.slice(1)}</h1>
    </div>

    <input type="text" bind:value={idInput} placeholder="id">

    <button on:click={() => handleButtonClick('s')}>All</button>  <!-- Default query button (all rows) -->
    {#each columns as column}
        <button on:click={() => handleButtonClick('/'+column+'={}')}>{column}</button>
    {/each}


    <!--{#if show_card}-->
    <!--    <SItemCard-->
    <!--        id={idInput}-->
    <!--        name={nameInput}-->
    <!--        data={l_data-->
    <!--    />-->
    <!--{/if}-->

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
