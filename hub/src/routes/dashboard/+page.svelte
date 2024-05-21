<script>

    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { api_url, access_token, current_table, current_tab } from '../../stores.js';
    import UserCard from './UserCard.svelte';
    import SomeTable from './SomeTable.svelte';
    import SchemaSelector from './SchemaSelector.svelte';
import DataView from "./DataView.svelte";

    let apiUrl;
    $: api_url.subscribe(value => apiUrl = value);

    let token;
    $: access_token.subscribe(value => token = value);


    let selectedTable = ''; // For the selected table
    let tables = {};

    // let tableData = []; // To store the fetched table data
    // let columns = []; // To store the table columns

    onMount(() => {if (!token) {goto('/');}});




    let currentTab = 'All';

</script>

<main class="mx-auto p-8 flex space-x-8">
    <div class="w-1/3">
        {#if token}
            <UserCard {token} />
            <SchemaSelector {tables} />
        {:else}<div class="mt-4 text-gray-500 text-sm">Loading...</div>{/if}
    </div>
    <div class="w-2/3">
    <DataView/>
    </div>
</main>
