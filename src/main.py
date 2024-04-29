"""
Main file for the FastAPI application

This file is the entry point for the FastAPI application. It is responsible for creating the FastAPI application and running it.
"""
# ? External
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# ? Local
from src.routes import *
from src.config import Config


app = FastAPI(
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

app.add_middleware(  # Add CORS middleware
    CORSMiddleware,
    # allow_origins=get_cors_origins(),
    allow_origins="http://localhost:8080",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ? Test the Auth route...
# * Improve the security by adding a token to the login route to authenticate the user & authorize them to access the application.
from src.model.auth import create_token, DEFAULT_USER, JWTBearer
from pydantic import BaseModel







@app.post("/token", tags=["Auth"])
def get_test_token():
    # return JSONResponse(content={"token": create_token(DEFAULT_USER)})
    return {"access_token": create_token(DEFAULT_USER)}

# * Example of a protected route
@app.get("/protected", dependencies=[Depends(JWTBearer())])
def protected_route():
    return {"message": "You are viewing a protected route"}






# * Create routes
app.include_router(home)  # * main routes for the application...
app.include_router(basic_dt)
# app.include_router(crud_attr)
# app.include_router(views, prefix="/views")


# * Run the application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
