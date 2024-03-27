<h1 align="center">
    <img src="./assets/icons/diary.png" alt="Academic Hub Icon" width="128">
    <div align="center">Academic Hub</div>
</h1>

[<img alt="github" src="https://img.shields.io/badge/github-Yrrrrrf%2Facademic__hub-58A6FF?style=for-the-badge&logo=github" height="24">](https://github.com/Yrrrrrf/academic_hub)

[//]: # ([<img alt="documentation" src="https://img.shields.io/badge/documentation-100%25-66c2a5?style=for-the-badge&logo=read-the-docs&labelColor=555555" height="24">]&#40;#documentation-section&#41;)

Academic Hub is a comprehensive platform designed to manage academic resources and data, including library inventory, academic user information (students, teachers, etc.), grades history, and more. The system is built on a relational database, supporting various academic operations and providing detailed reports for educational institutions.

## Setup

### Prerequisites

- Install the [PostgreSQL](https://www.postgresql.org/download/) database server and used files inside the [sql](./sql) folder to create the database schema and populate it with sample data.


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
## [License](./LICENSE)

This project is licensed under the terms of the MIT license.
