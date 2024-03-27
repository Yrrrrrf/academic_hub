<script>
    import { Link } from "svelte-routing";

//     create the links for Home and About
//     const links = [
//         { name: "Home", href: "/" },
//         { name: "About", href: "/about" },
//     ];
//
//

</script>

<div class="superior-bar">
    <img src="favicon.png" alt="Logo" class="logo">
</div>


<style>
    /* Optional: Add some styles to make the buttons look like navigation buttons */
    button {
        margin: 0 10px;
        padding: 10px 20px;
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
    }

    button:hover {
        background-color: #0056b3;
    }

    .logo {
        width: 128px;
        height: 128px;
    }

    .superior-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 2rem;
        background-color: #aaaaaa;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
</style>
