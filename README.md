<h1 align="center">
    <!-- <img src="resources/img/library.gif" alt="Library" width="192"> -->
    <img src="./assets/icons/books.png" alt="Library Inventory Management" width="192">
    <div align="center">Library Inventory Management</div>
</h1>

[<img alt="github" src="https://img.shields.io/badge/github-LibraryInventory%2Fmanagement-58A6FF?style=for-the-badge&logo=github" height="24">](https://github.com/LibraryInventory/management)
<!-- [<img alt="documentation" src="https://img.shields.io/badge/documentation-100%25-66c2a5?style=for-the-badge&logo=read-the-docs&labelColor=555555" height="24">](#documentation-section)
 -->

Library Inventory Management is a comprehensive solution for managing libraries, designed to handle the inventory of books, process loans, manage user information, and provide detailed reports.  

The system is built on a relational database, supporting operations such as registering new books, tracking loaned books, and generating various reports for library staff.  

## Setup

### Prerequisites

- Use the latest version of [Python](https://www.python.org/downloads/).
- Install the required packages using the following command:
```bash
# using pip
pip install -r requirements.txt  # using pip
# using conda or mamba
conda install --file requirements.txt  # using conda
mamba install --file requirements.txt  # using mamba
```

- Configure the database connection creating the [.env](./.env) file with the following content:
```bash
DB_NAME = "database_name"  # the name of the database to connect to
USER = "database_user"  # the user to connect to the database
PASSWORD = "user_password"  # the password for the user 
HOST = "localhost"  # the host where the database is running (default: localhost)
```

## Features

- **Catalog Management**: Manage the catalogs for books, authors, publishers, and library branches.
- **Loan Processing**: Record and track the loaning of books to users, including due dates and return processing.
- **Reporting**: Generate reports on book availability, loan activity, popular titles, and user activity.
- **Search Functionality**: Provide powerful search capabilities across books, authors, and publishers.

## [License](./LICENSE)

This project is licensed under the terms of the MIT license.
