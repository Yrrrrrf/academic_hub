<!--<script>-->
<!--    import { onMount } from 'svelte';-->
<!--    import SItemCard from "./SItemCard.svelte";-->
<!--    let dts = [];-->
<!--    export let table_name;-->

<!--    let columns = [];-->
<!--    // fetch the columns from the server and assign to columns-->
<!--    // http://localhost:8000/${table_name}/dt/ -> to get the column names-->

<!--    async function get_columns() {-->
<!--        let fetchUrl = `http://localhost:8000/${table_name}/dt/`;-->
<!--        const response = await fetch(fetchUrl);-->
<!--        columns = await response.json();-->
<!--    }-->

<!--    onMount(async () => {-->
<!--        await get_columns();-->
<!--    });-->

<!--    let rows = [];-->
<!--    async function fetch_dts() {-->
<!--        let fetchUrl = `http://localhost:8000/${table_name}`;-->
<!--        fetchUrl += `${attr}`;-->

<!--        const response = await fetch(fetchUrl);-->
<!--        dts = await response.json();-->

<!--        columns = Object.keys(dts[0]);-->
<!--        rows = dts.map(dt => Object.values(dt));-->
<!--    }-->
<!--</script>-->

<!--&lt;!&ndash;list the &ndash;&gt;-->

<!--&lt;!&ndash;<h1>{table_name}</h1>&ndash;&gt;-->

<!--&lt;!&ndash;<button on:click={() => {&ndash;&gt;-->
<!--&lt;!&ndash;    attr = 's/';&ndash;&gt;-->
<!--&lt;!&ndash;    fetch_dts();&ndash;&gt;-->
<!--&lt;!&ndash;}}>All&ndash;&gt;-->
<!--&lt;!&ndash;</button>&ndash;&gt;-->

<!--&lt;!&ndash;<SItemCard columns={columns} rows={rows} />&ndash;&gt;-->

<!--&lt;!&ndash;<button on:click={() => {&ndash;&gt;-->
<!--&lt;!&ndash;    attr = '/id=1';&ndash;&gt;-->
<!--&lt;!&ndash;    fetch_dts();&ndash;&gt;-->
<!--&lt;!&ndash;}}>byId&ndash;&gt;-->
<!--&lt;!&ndash;</button>&ndash;&gt;-->

<!--&lt;!&ndash;<button on:click={() => {&ndash;&gt;-->
<!--&lt;!&ndash;    attr = '/name=Robert W. Johnson';&ndash;&gt;-->
<!--&lt;!&ndash;    fetch_dts();&ndash;&gt;-->
<!--&lt;!&ndash;}}>byName&ndash;&gt;-->
<!--&lt;!&ndash;&gt;</button>&ndash;&gt;-->

<!--<style>-->
<!--    /* Overall Page Styling */-->
<!--    body {-->
<!--        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;-->
<!--        padding: 20px;-->
<!--        background-color: #f4f4f4;-->
<!--        color: #333;-->
<!--    }-->

<!--    h1 {-->
<!--        color: #333;-->
<!--    }-->

<!--    /* Table Styling */-->
<!--    table {-->
<!--        border-collapse: collapse;-->
<!--        width: 100%;-->
<!--        margin-top: 20px;-->
<!--        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);-->
<!--    }-->

<!--    th, td {-->
<!--        border: 1px solid #dddddd;-->
<!--        text-align: left;-->
<!--        padding: 12px;-->
<!--    }-->

<!--    th {-->
<!--        background-color: #6200EE;-->
<!--        color: white;-->
<!--        text-transform: uppercase;-->
<!--    }-->

<!--    tr:nth-child(even) {-->
<!--        background-color: #f2f2f2;-->
<!--    }-->

<!--    /* Button Styling */-->
<!--    button {-->
<!--        padding: 10px 20px;-->
<!--        border: none;-->
<!--        border-radius: 5px;-->
<!--        background-color: #6200EE;-->
<!--        color: white;-->
<!--        cursor: pointer;-->
<!--        margin-right: 10px;-->
<!--        transition: background-color 0.3s ease;-->
<!--    }-->

<!--    button:hover {-->
<!--        background-color: #7b1fa2;-->
<!--    }-->

<!--    /* Column List Styling - Assuming you still want to list columns separately */-->
<!--    li {-->
<!--        background-color: #eee;-->
<!--        margin: 5px 0;-->
<!--        padding: 10px;-->
<!--        border-radius: 5px;-->
<!--        list-style: none;-->
<!--    }-->
<!--</style>-->

<!--{#if dts && dts.length > 0}-->
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
<!--                {#each row as cell}-->
<!--                    <td>{cell}</td>-->
<!--                {/each}-->
<!--            </tr>-->
<!--        {/each}-->
<!--        </tbody>-->
<!--    </table>-->
<!--{:else}-->
<!--&lt;!&ndash;    <p>No data to display.</p>&ndash;&gt;-->
<!--{/if}-->
