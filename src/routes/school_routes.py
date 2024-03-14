from fastapi import APIRouter


by_attribute: APIRouter = APIRouter()
"""
# By Attribute Route
This route contains all the CRUD methods that involve any query `by attribute`

This means thaat the route will contain methods that will query the database by a specific attribute

## Example
- Get all the books (by any attribute)
- Get all the authors (by any attribute)
"""

school_views: APIRouter = APIRouter()
"""
# View Route
This route contains the READ methods that involve viewing the database

The views will be used to display complex queries that involve multiple tables.
These views will be used to display the data in the frontend in a user-friendly manner. 

## Example
- Get all the books with their authors and publishers
- Get all the books with their topics and libraries
- Get all the books with their authors, topics, and libraries
- Get all the books with their authors, topics, libraries, and publishers
"""

