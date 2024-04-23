"""
Main file for the FastAPI application

This file is the entry point for the FastAPI application. It is responsible for creating the FastAPI application and running it.
"""
# ? External
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ? Local
# from src.routes import school, library, general, setup
from src.config import Config


# Create the FastAPI application
app = FastAPI(
#     # Create the database and tables
    title = Config.NAME.value,
    description = Config.DESCRIPTION.value,
    version = Config.VERSION.value,
    contact = {
        "name": Config.AUTHOR.value, 
        "email": Config.EMAIL.value
        },
    license_info={
        "name": "MIT",
        "url": "https://choosealicense.com/licenses/mit/",
    },
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    # allow_origins=get_cors_origins(),
    allow_origins="http://localhost:8080",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# * Create routes
# * create_routes(app)
from src.routes import home, basic_dt, by_attr, views


app.include_router(home)
app.include_router(basic_dt)
app.include_router(by_attr)
app.include_router(views, prefix="/views")


# Run the application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
