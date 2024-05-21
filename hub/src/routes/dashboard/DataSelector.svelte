<script>
    import { ListBox, ListBoxItem } from '@skeletonlabs/skeleton';
    import { api_url, current_table } from "../../stores.js";
    import { onMount } from "svelte";

    let apiUrl;
    $: api_url.subscribe(value => apiUrl = value);

    let currentTable = '';
    let currentSchema = '';
    let tables = [];

    let schemas = [
        {
            name: 'School',
            icon: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 2L1 7L12 12L23 7L12 2ZM12 22V12.75M1 7V17L12 22M23 7V17L12 22" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
        },
        {
            name: 'Library',
            icon: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M5 4V20M19 4V20M5 4H19M5 20H19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
        },
        {
            name: 'Infrastructure',
            icon: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4 4H20M4 10H20M4 16H20M4 22H20M4 4V22M20 4V22" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
        },
    ];

    function snakeToCamelWithSpaces(str) {
        return str
            .split('_')
            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
            .join(' ');
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
                tables = data.map(snakeToCamelWithSpaces);
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

    function updateSelectedTable() {
        current_table.set(currentTable);
        console.log('Selected table:', currentTable);
    }

</script>

<h2 class="pt-16 pb-4 text-xl">Select Schema</h2>

<ListBox>
    {#each schemas as schema}
        <ListBoxItem bind:group={currentSchema} name="schema" value={schema.name}>
            {@html schema.icon} {schema.name}
        </ListBoxItem>
    {/each}
</ListBox>

{#if tables.length > 0}
    <div class="mt-4">
        <h3 class="text-lg">Select Table</h3>
        <ListBox>
            {#each tables as table}
                <ListBoxItem bind:group={currentTable} name="table" value={table} on:change={updateSelectedTable}>
                    {table}
                </ListBoxItem>
            {/each}
        </ListBox>
    </div>
{:else}
    <p class="mt-4">No tables available for the selected schema.</p>
{/if}

<style>
    .mt-4 {
        margin-top: 1rem;
    }
    .text-lg {
        font-size: 1.125rem;
    }
    .text-xl {
        font-size: 1.25rem;
    }
</style>
