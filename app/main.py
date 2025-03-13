import json
import uvicorn
from fastapi import FastAPI

from app.database import users_db
from app.models.User import User
from routers import status, users

app = FastAPI()
app.include_router(status.router)
app.include_router(users.router)


if __name__ == "__main__":
    with open("users.json") as f:
        users_db.extend(json.load(f))

    for user in users_db:
        User.model_validate(user)

    print("Users loaded")

    uvicorn.run(app, host="localhost", port=8002)

