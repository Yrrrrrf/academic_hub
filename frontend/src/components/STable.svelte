<script>
    import { onMount } from 'svelte';
    let books = [];

    async function fetchBooks() {
        const response = await fetch('http://127.0.0.1:8000/books/');
        books = await response.json();
    }
</script>

<button on:click="{fetchBooks}">Load Books</button>

{#if books.length > 0}
    <ul>
        {#each books as book}
            <li>{book.nombre}</li>
        {/each}
    </ul>
{:else}
    <p>No books to display.</p>
{/if}
