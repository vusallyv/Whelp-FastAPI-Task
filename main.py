from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import routers
from db import models
from db import database
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(routers.router)


database.db.connect()
database.db.create_tables([models.IPAddress, models.User])
database.db.close()
