<script>
    import { Tab, TabGroup, ListBox, ListBoxItem } from "@skeletonlabs/skeleton";
    import SomeTable from './SomeTable.svelte';
    import { api_url, current_table, current_tab, current_schema } from "../../stores.js";
    import { onMount } from "svelte";

    let apiUrl = '';
    $: api_url.subscribe(value => apiUrl = value);

    let currentSchema = '';
    $: current_schema.subscribe(value => currentSchema = value);

    let currentTab = '';
    $: current_tab.subscribe(value => currentTab = value);

    let currentTable = '';
    $: current_table.subscribe(value => currentTable = value);


    let tabs = ['all', 'views', 'some', 'other'];

    let columns = [];
    let tableData = [];

    let tables = {};

    function snakeToCamelWithSpaces(str) {
        return str
            .split('_')
            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
            .join(' ');
    }

    async function fetchTableRows(table) {
        const request_url = `${apiUrl}/${table.replace(/ /g, '_').toLowerCase()}s`;
        console.log('Request URL:', request_url);
        try {
            const response = await fetch(request_url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            if (response.ok) {
                const data = await response.json();
                tableData = data;
                columns = Object.keys(data[0] || {}); // Keep original keys
                console.log(`Rows for ${table}:`, data);
            } else {
                throw new Error('Failed to fetch rows');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }

    async function fetchTables(schema) {
        const request_url = `${apiUrl}/${schema}/tables`;
        console.log('Request URL:', request_url);
        try {
            const response = await fetch(request_url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            if (response.ok) {
                const data = await response.json();
                tables = { ...tables, [schema]: data.map(snakeToCamelWithSpaces) };
                console.log(
                    schema.charAt(0).toUpperCase() + schema.slice(1),
                    'Tables:', data
                );
            } else throw new Error('Failed to fetch tables');
        } catch (error) {
            console.error('Error:', error);
        }
    }

    $: {
        if (currentSchema) {
            fetchTables(currentSchema.toLowerCase());
        }
    }

    function updateSelectedTab() {
        current_tab.set(currentTab);
        console.log('Selected tab:', currentTab);
        // fetchTables(currentSchema.toLowerCase());
    }

    function updateSelectedTable() {
        current_table.set(currentTable);
        console.log('Selected table:', currentTable);
        fetchTableRows(currentTable);
    }
</script>

<h1 class="text-2xl">{currentSchema} Data View</h1>

<TabGroup>
    {#each tabs as tab}
        <Tab bind:group={currentTab} name={tab} value={tab}
             on:change={updateSelectedTab}>{tab.toUpperCase()}
        </Tab>
    {/each}
</TabGroup>

{#if currentTab === 'all'}
    {#if currentSchema}
        {#if tables[currentSchema.toLowerCase()]}
            <div class="mt-4">
                <h3 class="text-lg">Select Table</h3>
                <ListBox>
                    {#each tables[currentSchema.toLowerCase()] as table}
                        <ListBoxItem bind:group={currentTable} name={table} value={table} on:change={updateSelectedTable}>
                            {table}
                        </ListBoxItem>
                    {/each}
                </ListBox>
            </div>
            <SomeTable {currentTable} {columns} {tableData}/>
        {/if}
    {/if}
{/if}
