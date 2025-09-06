from fastapi import FastAPI

from TodoApp import models
from TodoApp.database import engine
from TodoApp.routers import auth, todos

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
