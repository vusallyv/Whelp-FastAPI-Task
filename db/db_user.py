from fastapi import HTTPException
from db.hash import Hash
from db.models import User
from schemas import UserBase


def create_user(request: UserBase):
    username = request.username
    password = request.password
    email = request.email
    if not username:
        raise HTTPException(status_code=400, detail="Username is required")
    if not password:
        raise HTTPException(status_code=400, detail="Password is required")
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")
    user = User.filter(User.username == username).first()
    if user:
        raise HTTPException(status_code=400, detail="User already exists")
    user = User(username=username, password=Hash.bcrypt(
        password), email=email)
    user.save()
    return user
