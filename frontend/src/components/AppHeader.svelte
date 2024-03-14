<script>
    export let name; // Default app name, can be overridden by props
</script>

<header>
    <div class="header-container">
        <img class="app-icon" src="/favicon.png" alt="Library Management Icon" />
        <h1 class="app-name">{name}</h1>
    </div>
</header>

<style>
    header {
        background-color: #6200EE; /* Example color */
        color: white;
        padding: 10px 20px;
        display: flex;
        align-items: center;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }

    .header-container {
        display: flex;
        align-items: center;
        gap: 15px;
    }

    .app-icon {
        height: 48px; /* Adjust based on your icon's aspect ratio */
        /*height: 4em; !* Adjust based on your icon's aspect ratio *!*/
    }

    .app-name {
        margin: 0;
        font-size: 24px;
        font-weight: 500;
    }
</style>
