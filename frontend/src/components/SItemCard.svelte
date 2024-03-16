<script>
    export let title;
    export let description;
    export let image; // Assume an image URL is provided
</script>

<div class="card">
    <div class="img" style="background-image: url({image});"></div>
    <div class="save">
        <!-- Icon or save functionality goes here -->
        <!-- For example, a heart icon -->
        <svg class="svg" fill="currentColor" viewBox="0 0 20 20">
            <!-- Insert path data for a heart icon or use an <img> tag -->
        </svg>
    </div>
    <div class="text">
        <h3 class="h3">{title}</h3>
        <p class="p">{description}</p>
        <!-- Example interactive icon box -->
        <div class="icon-box">
            <svg><!-- SVG content --></svg>
            <span class="span">Some action</span>
        </div>
    </div>
</div>

<style>
    /* Your CSS goes here */
</style>
