from fastapi import APIRouter


home: APIRouter = APIRouter()
"""
# Home Route

This route contains the main methods that will be used to display the home page of the application.

## Example
- Get the home page
- Get the about page
- Get the contact page
- Get the help page
"""

# create an example route that shows the name of the application
@home.get("/", tags=["home"])
def read_root():
    return {"Hello From": "Home Route"}
