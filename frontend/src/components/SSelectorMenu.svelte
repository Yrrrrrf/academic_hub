<script>
    import { createEventDispatcher } from 'svelte';

    // Props for the dataset and the selected column name
    export let dataset = [];
    export let columnName = '';

    // State for the selected value
    let selectedValue = '';

    // Event dispatcher to inform parent components of the selection
    const dispatch = createEventDispatcher();

    // Function to handle the button click and dispatch the event
    function handleSelection() {
        dispatch('selected', { value: selectedValue });
    }

    // Derived array of unique values for the combo box based on the column
    $: uniqueValues = Array.from(new Set(dataset.map(item => item[columnName])));
</script>

<div class="selector-menu">
    <select bind:value={selectedValue}>
        <option disabled value="">Select a value</option>
        {#each uniqueValues as value}
            <option value={value}>{value}</option>
        {/each}
    </select>
    <button on:click={handleSelection}>Query</button>
</div>

<style>
    .selector-menu {
        margin: 1em 0;
        display: flex;
        justify-content: start;
        align-items: center;
    }

    select {
        margin-right: 1em;
        padding: 0.5em;
        border-radius: 5px;
        border: 1px solid #cccccc;
    }

    button {
        padding: 0.5em 1em;
        border-radius: 5px;
        border: none;
        background-color: #6200EE;
        color: white;
        cursor: pointer;
        transition: background-color 0.3s;
    }

    button:hover {
        background-color: #7b1fa2;
    }
</style>
