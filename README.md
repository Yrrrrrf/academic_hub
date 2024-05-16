<h1 align="center">
    <img src="./assets/icons/diary.png" alt="Academic Hub Icon" width="128">
    <div align="center">Academic Hub</div>
</h1>

[<img alt="github" src="https://img.shields.io/badge/github-Yrrrrrf%2Facademic__hub-58A6FF?style=for-the-badge&logo=github" height="24">](https://github.com/Yrrrrrf/academic_hub)

[//]: # ([<img alt="documentation" src="https://img.shields.io/badge/documentation-100%25-66c2a5?style=for-the-badge&logo=read-the-docs&labelColor=555555" height="24">]&#40;#documentation-section&#41;)

Academic Hub is a comprehensive platform designed to manage academic resources and data, including library inventory, academic user information (students, teachers, etc.), grade history, and more. The system is built on a relational database, supporting various academic operations and providing detailed reports for educational institutions.

## Setup

### Prerequisites

- Install the [PostgreSQL](https://www.postgresql.org/download/) database server and used files inside the [sql](./sql) folder to create the database schema and populate it with sample data.

- Use the latest version of [Python](https://www.python.org/downloads/).

- Use [npm](https://www.npmjs.com/get-npm) to run the frontend application.

### Installation

- Install the required packages using the following command:
```bash
# using pip
pip install -r requirements.txt  # using pip
# using conda or mamba
conda install --file requirements.txt  # using conda
mamba install --file requirements.txt  # using mamba
```

- Install the `npm` package manager and the `svelte` framework to run the frontend application.
```bash
cd hub  # change to the frontend directory (svelte app)
npm install  # install the required packages
```

- Configure the database connection creating the [.env](./.env) file with the following content:
```bash
DB_NAME = "database_name"  # the name of the database to connect to
HOST = "localhost"  # the host of the database

LIBRARY_USER = "library_user"  # the user for the library
LIBRARY_PSWD = "some_password"  # the password for the library user
SCHOOL_USER = "school_user"  # the user for the school
SCHOOL_PSWD = "somw_password"  # the password for the school user
```

## Database Schema

![db entity relationship diagram](./assets/static/db_erd.png)

## Running the Application

- Run the API server using the following command:
```bash
uvicorn src.main:app --reload --host 127.0.0.1 --port 8000
```
- Look for the API documentation at [port/docs#/](http://127.0.0.1:8000/docs#/)

- Excecute the frontend application using the following command:
```bash
cd hub  # change to the frontend directory (svelte app)
npm run dev  # run the frontend application
```
- Access the frontend application at [port 5173](http://localhost:5173/)

## [License](./LICENSE)

This project is licensed under the terms of the MIT license.
