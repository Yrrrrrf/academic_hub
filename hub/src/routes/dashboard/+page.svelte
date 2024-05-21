<script>

    function snakeToCamelWithSpaces(str) {
        return str
            .split('_')
            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
            .join(' ');
    }

        import { onMount } from 'svelte';
        import { goto } from '$app/navigation';
        import { api_url, access_token } from '../../stores.js';
        import UserCard from './UserCard.svelte';
        import SomeTable from './SomeTable.svelte';
        import SchemaSelector from './SchemaSelector.svelte';

        let apiUrl;
        $: api_url.subscribe(value => apiUrl = value);

        let token;
        let selectedPage = 'school';
        let selectedTable = ''; // For the selected table
        let tables = {};
        let tableData = []; // To store the fetched table data
        let columns = []; // To store the table columns

        $: access_token.subscribe(value => token = value);

        onMount(() => {
        if (!token) {
        goto('/');
    }
    });

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

        async function fetchTables(schema) {
        const request_url = `${apiUrl}/${schema}/tables`;
        console.log('Request URL:', request_url);
        try {
        const response = await fetch(request_url, {
        method: 'GET',
        headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
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

        async function fetchTableRows(table) {
        const request_url = `${apiUrl}/${table.replace(/ /g, '_').toLowerCase()}s/`;
        console.log('Request URL:', request_url);
        try {
        const response = await fetch(request_url, {
        method: 'GET',
        headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
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

        onMount(() => {
        schemas.forEach(schema => fetchTables(schema.name.toLowerCase()));
    });
</script>

<main class="mx-auto p-8 flex space-x-8">
    <div class="w-1/3">
        {#if token}
            <UserCard {token} />
            <SchemaSelector {schemas} {tables} bind:selectedTable={selectedTable} fetchTableRows={fetchTableRows} />
        {:else}<div class="mt-4 text-gray-500 text-sm">Loading...</div>{/if}
    </div>
    <div class="w-2/3">
        {#if token}
            {#if tableData.length > 0}<SomeTable {columns} {tableData} currentTable={selectedTable} />
            {:else}<div class="mt-4 text-gray-500 text-sm">No data available</div>{/if}
        {:else}<div class="mt-4 text-gray-500 text-sm">Loading...</div>{/if}
    </div>
</main>
