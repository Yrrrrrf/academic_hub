"""
Main file for the FastAPI application

This file is the entry point for the FastAPI application. It is responsible for creating the FastAPI application and running it.
"""
# ? External 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.model.library import author, book, loan_management, publisher, topic, user, library
# from .model.lib import loan_management

# ? Local
from src.routes import home, library_routes
from src.config import Config


# define the main function (entry point) for the FastAPI application
# in case we want to run the application using the command `python src/main.py`
# otherwise, we can use: `uvicorn src.main:app --reload --host 127.0.0.1 --port 8000`

# def run() -> None:
#     import uvicorn
#     uvicorn.run(app, host='127.0.0.1', port=8000)

# if __name__ == '__main__':
#     run()


def setup(api_app: FastAPI) -> None:
    """
    Setup the application by creating the database and tables
    """
    # Create the database and tables
    api_app.title = Config.NAME.value
    api_app.description = Config.DESCRIPTION.value
    api_app.version = Config.VERSION.value
    api_app.contact = {
        "name": Config.AUTHOR.value, 
        "email": Config.EMAIL.value
        }
    api_app.license_info = {"name": "MIT", "url": "https://choosealicense.com/licenses/mit/"}

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[  # * Define a list of allowed origins (the domains your frontend is served from)
            "http://localhost:8080",  #  *Add the origin for Svelte app here
        ],
        allow_credentials=True,  # Allow cookies
        allow_methods=["*"],  # Allow all methods
        allow_headers=["*"],  # Allow all headers
    )


# * Create the FastAPI application
app = FastAPI()
setup(app)  # Setup the application data

# * Add routes (endpoints) to the FastAPI application
app.include_router(home.home)
app.include_router(library_routes.by_attribute)
app.include_router(library_routes.library_views)

# * check if this is viable or not
# app.include_router(library.by_attribute, prefix="/lib")
# app.include_router(library.library_views, prefix="/lib")

