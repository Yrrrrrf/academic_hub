<script>
    import { onMount } from 'svelte';
    import SItemCard from "./SItemCard.svelte";

    export let table_name;  // Mandatory prop (name of the table)

    let columns = [];  // Define a reactive array if needed
    let rows = [];  // Define a reactive array if needed

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
        if (action.includes('{}')) {
            action = action.replace('{}', encodeURIComponent(inputVal));
        }

        let data = await fetch_data(action);
        if (data) {
            rows = data;
            show_card = true; // Assuming you want to show SItemCard now
        }
    }

        let inputVal = '';


</script>


<main>

    <div class="query-container">
        <h1>{table_name.charAt(0).toUpperCase() + table_name.slice(1)}</h1>
        <input type="text" bind:value={inputVal} placeholder="Enter query value" />
    </div>

        <button on:click={() => handleButtonClick('s/')}>All</button>  <!-- Default query button (all rows) -->
        {#each columns as column}
            <button on:click={() => handleButtonClick('/'+column+'={}')}>{column}</button>
        {/each}

    {#if show_card && rows.length > 0}
        <table>
            <thead>
            <tr>
                {#each columns as column}
                    <th>{column}</th>
                {/each}
            </tr>
            </thead>
            <tbody>
            {#each rows as row}
                <tr>
                    {#each columns as column}
                        <td>{row[column]}</td> <!-- Access row data by column key -->
                    {/each}
                </tr>
            {/each}
            </tbody>
        </table>
    {/if}

    <!--{#if show_card && rows.length > 0}-->
    <!--    <table>-->
    <!--        <thead>-->
    <!--        <tr>-->
    <!--            {#each columns as column}-->
    <!--                <th>{column}</th>-->
    <!--            {/each}-->
    <!--        </tr>-->
    <!--        </thead>-->
    <!--        <tbody>-->
    <!--        {#each rows as row}-->
    <!--            <tr>-->
    <!--                {#each Object.values(row) as value}-->
    <!--                    <td>{value}</td>-->
    <!--                {/each}-->
    <!--            </tr>-->
    <!--        {/each}-->
    <!--        </tbody>-->
    <!--    </table>-->
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

    table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
    }

    th, td {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: left;
    }

    th {
        background-color: #FB8C00;
        color: white;
    }

    tr:nth-child(odd) {
        background-color: #FFF3E0;
    }

</style>
