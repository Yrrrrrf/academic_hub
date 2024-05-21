<script>
    import { Accordion, AccordionItem, ListBox, ListBoxItem } from '@skeletonlabs/skeleton';

    export let schemas = [];
    export let tables = {};
    export let selectedTable = '';
    export let fetchTableRows;
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
                            <ListBoxItem bind:group={selectedTable} name="table" value={table} on:click={() => fetchTableRows(table)}>
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
