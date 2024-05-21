<script>
    export let columns = [];
    export let tableData = [];
    export let currentTable = ''; // New prop to hold the current table name

    // Function to capitalize the first letter of the table name
    const capitalize = (str) => str.charAt(0).toUpperCase() + str.slice(1);
</script>

<p class="p-4 text-xl font-extrabold">{capitalize(currentTable)}</p>

<div class="table-container">
    <table class="table table-hover">
        <thead>
        <tr>
            {#each columns as column}
                <th class="px-4 py-2">{column}</th>
            {/each}
        </tr>
        </thead>
        <tbody>
        {#each tableData as row}
            <tr>
                {#each columns as column}
                    <td class="px-4 py-2">{row[column]}</td>
                {/each}
            </tr>
        {/each}
        </tbody>
    </table>
</div>
