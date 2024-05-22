<script>
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { access_token, current_table, current_schema } from '../../stores.js';
    import UserCard from './UserCard.svelte';
    import DataView from "./DataView.svelte";
    import {ListBox, ListBoxItem} from "@skeletonlabs/skeleton";

    let currentSchema = '';
    $: current_table.subscribe(value => currentSchema = value);

    let token;
    $: access_token.subscribe(value => token = value);

    let schemas = [
        {
            name: 'public',
            // icon: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 2L2 7L12 12L22 7L12 2ZM12 22V12.75M2 7V17L12 22M22 7V17L12 22" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
        },
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

    onMount(() => {if (!token) {goto('/');}});

    function updateSchema() {
        current_schema.set(currentSchema);
        console.log('Current schema:', currentSchema);
    }

</script>


<main class="mx-auto p-8 flex space-x-8">
    <div class="w-1/3">
        {#if token}
            <UserCard {token} />
        {:else}<div class="mt-4 text-gray-500 text-sm">Loading...</div>{/if}

        <h2 class="pt-16 pb-4 text-xl">Select Schema</h2>
        <ListBox>
            {#each schemas as schema}
                <ListBoxItem bind:group={currentSchema} name={schema.name} value={schema.name} on:change={updateSchema}>
                    {@html schema.icon} {schema.name}
                </ListBoxItem>
            {/each}
        </ListBox>
    </div>
    <div class="w-2/3">
        <DataView/>
    </div>
</main>
