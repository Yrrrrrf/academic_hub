<script>
    import { Tab, TabGroup, ListBox, ListBoxItem } from "@skeletonlabs/skeleton";
    import SomeTable from './SomeTable.svelte';
    import { api_url, current_table, current_tab, current_schema, current_view } from "../../stores.js";
    import { onMount } from "svelte";

    let apiUrl = '';
    $: api_url.subscribe(value => apiUrl = value);

    let currentView = '';
    $: current_view.subscribe(value => currentView = value);

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
    let views = {};

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

    async function fetchViews(schema) {
        const request_url = `${apiUrl}/${schema}/views`;
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
                views = { ...views, [schema]: data.map(snakeToCamelWithSpaces) };
                console.log(
                    schema.charAt(0).toUpperCase() + schema.slice(1),
                    'Views:', data
                );
            } else {
                throw new Error('Failed to fetch views');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }

    function resetTable() {
        tableData = [];
        columns = [];
    }

    $: {
        if (currentSchema) {
            resetTable();
            fetchTables(currentSchema.toLowerCase());
            fetchViews(currentSchema.toLowerCase());
        }
    }

    $: {
        if (currentTab) {
            resetTable();
        }
    }

    async function fetchViewRows(view) {
        const request_url = `${apiUrl}/${currentSchema.toLowerCase()}/view/${view.replace(/ /g, '_').toLowerCase()}`;
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
                console.log(`Rows for ${view}:`, data);
            } else {
                throw new Error('Failed to fetch rows');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }

    function updateSelectedTab() {
        current_tab.set(currentTab);
        console.log('Selected tab:', currentTab);
    }

    function updateSelectedView() {
        current_view.set(currentView);
        console.log('Selected view:', currentView);
        fetchViewRows(currentView);
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

{#if currentTab === 'all' && currentSchema && tables[currentSchema.toLowerCase()]}
    <ListBox>
        <div class="mt-4 flex flex-wrap gap-4">
            {#each tables[currentSchema.toLowerCase()] as table}
                <ListBoxItem
                        bind:group={currentTable}
                        name={table}
                        value={table}
                        class="mt-4 variant-filled-primary"
                        on:change={updateSelectedTable}>
                    {table}
                </ListBoxItem>
            {/each}
        </div>
    </ListBox>
    <SomeTable {currentTable} {columns} {tableData}/>
{/if}

{#if currentTab === 'views' && currentSchema && views[currentSchema.toLowerCase()]}
    <ListBox>
        <div class="mt-4 flex flex-wrap gap-4">
            {#each views[currentSchema.toLowerCase()] as view}
                <ListBoxItem
                        bind:group={currentView}
                        name={view}
                        value={view}
                        class="mt-4 variant-filled-primary"
                        on:change={updateSelectedView}>
                    {view}
                </ListBoxItem>
            {/each}
        </div>
    </ListBox>
    <SomeTable {currentView} {columns} {tableData}/>
{/if}
