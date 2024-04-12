"""
Main file for the FastAPI application

This file is the entry point for the FastAPI application. It is responsible for creating the FastAPI application and running it.
"""
# ? External 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# ? Local
from src.routes import home, library, school
from src.config import Config


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
        CORSMiddleware,  # * Add the CORS middleware to the application
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
# Add routes for the home page
app.include_router(home.home)

# # Add routes for the library model
# app.include_router(library.basic_dt)
# app.include_router(library.by_attr)
# app.include_router(library.views)
# app.include_router(library.views, prefix="/lib")

# # Add routes for the school model
app.include_router(school.basic_dt)
app.include_router(school.by_attr)
# app.include_router(school.views)
app.include_router(school.views, prefix="/school")


# * check if this is viable or not

# Define the main function (entry point) for the FastAPI application
# in case we want to run the application using the command `python src/main.py`
# otherwise, we can use: `uvicorn src.main:app --reload --host 127.0.0.1 --port 8000`

# def run() -> None:
#     import uvicorn
#     uvicorn.run(app, host='127.0.0.1', port=8000)

# if __name__ == '__main__':
#     run()
