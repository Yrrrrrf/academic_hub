<script>
    export let currentTable = 'Some Table...'; // New prop to hold the current table name
    export let columns = [];
    export let tableData = [];

    // Function to capitalize the first letter of the table name
    const capitalize = (str) => str.charAt(0).toUpperCase() + str.slice(1);
</script>

<p class="p-4 text-xl font-extrabold">{capitalize(currentTable)}</p>

{#if tableData.length > 0}
    <div class="table-container">
        <table class="table table-hover">
            <thead>
            <tr>
                {#each columns as column}
                    <th>{column}</th>
                {/each}
            </tr>
            </thead>
            <tbody>
            {#each tableData as row}
                <tr>
                    {#each columns as column}
                        <td>{row[column]}</td>
                    {/each}
                </tr>
            {/each}
            </tbody>
        </table>
    </div>
{:else}
    <div class="mt-4 text-gray-500 text-sm">No data available</div>
{/if}
