"""
Main file for the FastAPI application

This file is the entry point for the FastAPI application. It is responsible for creating the FastAPI application and running it.
"""
# ? External 
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

# ? Local
from src.routes import school, library, general, setup
from src.config import Config


def setup_api(api_app: FastAPI) -> None:
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

def setup_routes(api_app: FastAPI) -> None:
    """
    Setup the routes for the FastAPI application
    """
    api_app.include_router(setup.home)




    dt: APIRouter = APIRouter()
    attr: APIRouter = APIRouter()
    views: APIRouter = APIRouter()

    dt.include_router(general.basic_dt)
    dt.include_router(library.basic_dt)
    dt.include_router(school.basic_dt)

    attr.include_router(general.by_attr)
    attr.include_router(library.by_attr)
    attr.include_router(school.by_attr)

    views.include_router(general.views)
    views.include_router(library.views)
    views.include_router(school.views)




    # api_app.include_router(dt)
    # api_app.include_router(attr)
    # api_app.include_router(views)

    # # * Add routes (endpoints) to the FastAPI application
    # # Add routes for the home page
    # # api_app.include_router(setup.docs)

    # api_app.include_router(general.basic_dt)
    # api_app.include_router(general.by_attr)
    # api_app.include_router(general.views)
    # # api_app.include_router(general.all)
    # # api_app.include_router(general.auth)

    # # api_app.include_router(library.basic_dt)
    # # api_app.include_router(library.by_attr)
    # # api_app.include_router(library.views)
    # # api_app.include_router(library.all)

    api_app.include_router(school.basic_dt)
    # api_app.include_router(school.by_attr)
    # # api_app.include_router(school.views)
    # # api_app.include_router(school.all)


# * Create the FastAPI application

app = FastAPI()

setup_api(app)  # Setup the application data
setup_routes(app)  # Setup the application routes


# * check if this is viable or not

# Define the main function (entry point) for the FastAPI application
# in case we want to run the application using the command `python src/main.py`
# otherwise, we can use: `uvicorn src.main:app --reload --host 127.0.0.1 --port 8000`

# def run() -> None:
#     import uvicorn
#     uvicorn.run(app, host='127.0.0.1', port=8000)

# if __name__ == '__main__':
#     run()
