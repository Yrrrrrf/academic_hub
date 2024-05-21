<script>
    import { Tab, TabGroup } from "@skeletonlabs/skeleton";
    import SomeTable from './SomeTable.svelte';

    import { api_url, current_tab, current_table } from '../../stores.js';

    let apiUrl;
    $: api_url.subscribe(value => apiUrl = value);

    let currentTable = '';
    $: current_table.subscribe(value => currentTable = value);

    let currentTab = '';
    $: current_tab.subscribe(value => currentTab = value);

    // export let token;

    // export let columns;
    // export let tableData;

    //
    // async function fetchTableRows(table) {
    //     const request_url = `${apiUrl}/${table.replace(/ /g, '_').toLowerCase()}s`;
    //     console.log('Request URL:', request_url);
    //     try {
    //         const response = await fetch(request_url, {
    //             method: 'GET',
    //             headers: {
    //                 'Content-Type': 'application/json',
    //                 'Authorization': `Bearer ${token}`
    //             }
    //         });
    //         if (response.ok) {
    //             const data = await response.json();
    //             tableData = data;
    //             columns = Object.keys(data[0] || {}); // Keep original keys
    //             console.log(`Rows for ${table}:`, data);
    //         } else {
    //             throw new Error('Failed to fetch rows');
    //         }
    //     } catch (error) {
    //         console.error('Error:', error);
    //     }
    // }


    function updateSelectedTab() {
        current_tab.set(currentTab);
        console.log('Selected tab:', currentTab);
    }

    let tabs = [
        'All',
        'Views',
        'Some',
        'Other'
    ];

    function printData() {
        console.log(currentTable, currentTab);
    }

</script>

<div class="w-2/3">
    <TabGroup>
        {#each tabs as tab}
            <Tab bind:group={currentTab} name={tab.toLowerCase()} value={tab} on:change={updateSelectedTab}>{tab}</Tab>
        {/each}
    </TabGroup>


    <button class="btn variant-glass-primary" on:click={printData}>Penchs</button>

    <!--    {#if token}-->
<!--        {#if tableData.length > 0}-->
<!--            <SomeTable {columns} {tableData} currentTable={selectedTable} />-->
<!--        {:else}-->
<!--            <div class="mt-4 text-gray-500 text-sm">No data available</div>-->
<!--        {/if}-->
<!--    {:else}-->
<!--        <div class="mt-4 text-gray-500 text-sm">Loading...</div>-->
<!--    {/if}-->
</div>
