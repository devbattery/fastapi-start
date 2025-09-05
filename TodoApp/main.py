from fastapi import FastAPI

from TodoApp import models
from TodoApp.database import engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)
