<script>
    import { Accordion, AccordionItem, ListBox, ListBoxItem } from '@skeletonlabs/skeleton';

    import { api_url, current_table } from "../../stores.js";
    import {onMount} from "svelte";

    let apiUrl;
    $: api_url.subscribe(value => apiUrl = value);

    let currentTable = '';


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

    export let tables = {};


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
                tables = { ...tables, [schema]: data.map(snakeToCamelWithSpaces) };
                console.log('Tables:', data);
            } else {
                throw new Error('Failed to fetch tables');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }




    onMount(() => {schemas.forEach(schema => fetchTables(schema.name.toLowerCase()));});

    function updateSelectedTable() {
        current_table.set(currentTable);
        console.log('Selected table:', currentTable);
    }

</script>

<h2 class="pt-16 pb-4 text-xl">Select Schema</h2>

<Accordion autoCollapse>
    {#each schemas as schema}
        <AccordionItem>
            <svelte:fragment slot="lead">
                {@html schema.icon}
            </svelte:fragment>
            <svelte:fragment slot="summary">{schema.name}</svelte:fragment>
            <svelte:fragment slot="content">
                {#if tables[schema.name.toLowerCase()]}
                    <ListBox>
                        {#each tables[schema.name.toLowerCase()] as table}
                            <ListBoxItem bind:group={currentTable} name="table" value={table} on:change={updateSelectedTable}>
                                {table}
                            </ListBoxItem>
                        {/each}
                    </ListBox>
                {:else}
                    <p>Loading tables...</p>
                {/if}
            </svelte:fragment>
        </AccordionItem>
    {/each}
</Accordion>
