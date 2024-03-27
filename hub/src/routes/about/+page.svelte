<!-- About.svelte -->
<script>
	import logo from '$lib/images/diary.png';
</script>

<div class="container">
	<h1>
		<img src={logo} alt="Academic Hub" width="192">
		Academic Hub
	</h1>
	<p>Meant to be a comprehensive solution for managing libraries, designed to handle the inventory of books, process loans, manage user information, and provide detailed reports.</p>

	<h2>Features</h2>
	<li>The system is built on a relational database, supporting operations such as registering new books, tracking loaned books, and generating various reports for library staff.</li>
	<li>It also includes a school management system, which allows users to manage student information, track attendance, and generate reports for teachers and administrators.</li>

	<h2>License</h2>
	<p>This project is licensed under the terms of the <a href="./LICENSE">MIT license</a>.</p>

	<h2>Source Code</h2>
	<p>For more information, you can visit the <a href="https://github.com/LibraryInventory/management">GitHub repository</a>.</p>
</div>

<style>
	/* Container styles */
	.container {
		max-width: 800px;
		margin: 0 auto;
		padding: 20px;
		font-family: 'Arial', sans-serif;
	}

	/* Heading styles */
	h1 {
		text-align: center;
		margin-bottom: 20px;
	}

	/* Image styles */
	img {
		display: block;
		margin: 0 auto;
		border-radius: 8px;
		margin-bottom: 20px;
	}

	/* Feature list styles */
	ul {
		list-style-type: disc;
		margin-left: 20px;
		margin-bottom: 20px;
	}

	li {
		margin-bottom: 10px;
	}

	/* Code block styles */
	pre {
		background-color: #f4f4f4;
		padding: 10px;
		border-radius: 8px;
		overflow-x: auto;
	}

	/* Link styles */
	a {
		color: #0077cc;
		text-decoration: none;
		transition: color 0.3s ease;
	}

	a:hover {
		color: #005299;
	}

	/* License section styles */
	h2 {
		border-bottom: 2px solid #ddd;
		padding-bottom: 10px;
		margin-bottom: 20px;
	}

	/* Paragraph styles */
	p {
		line-height: 1.6;
		margin-bottom: 20px;
	}
</style>
