import datetime
from fastapi import APIRouter, Depends, HTTPException
from db.db_user import create_user
from db.hash import Hash
from db.models import User
from schemas import UserBase, UserDisplay, UserLogin
from tasks.tasks import create_task
from db.db_ip_address import get_status_of_task
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel


router = APIRouter(
    prefix="/api/v1",
    tags=["api"]
)


class Settings(BaseModel):
    authjwt_secret_key: str = "aab14302905e5ff87d459f78bf851dffff88adf0c4f360011d17897e8fdf53a6"


@AuthJWT.load_config
def get_config():
    return Settings()


@router.post('/login', description='JWT sign in')
def login(user: UserLogin, Authorize: AuthJWT = Depends()):
    if not user.username:
        raise HTTPException(status_code=400, detail="username not provided")
    if not user.password:
        raise HTTPException(status_code=400, detail="password not provided")
    user_in_db = User.filter(User.username == user.username).first()
    if not user_in_db:
        raise HTTPException(status_code=404, detail="User not found")
    if not Hash.bcrypt_verify(user.password, user_in_db.password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    expires = datetime.timedelta(days=1)
    access_token = Authorize.create_access_token(
        subject=user.username, expires_time=expires)
    refresh_token = Authorize.create_refresh_token(subject=user.username)
    return {"access_token": access_token, "token_type": "bearer", "expires_in (days)": expires.days, "refresh_token": refresh_token}


@router.post("/signup", response_model=UserDisplay, description="Create a user in MySQL DB")
def signup(request: UserBase):
    return create_user(request)


@router.get('/user')
def user(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        current_user = Authorize.get_jwt_subject()
        return {"user": current_user}
    except HTTPException:
        raise HTTPException(status_code=401, detail="Not authorized")


@router.post('/refresh')
def refresh(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()
        current_user = Authorize.get_jwt_subject()
        new_access_token = Authorize.create_access_token(subject=current_user)
        return {"access_token": new_access_token}
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid refresh token")


@router.post("/task", description="""
    Create a task in MySQL, send it to celery, and return task ID
    Input will be IP address of registered User.

    Create a free account on https://ipdata.co/
    Fetch data from https://ipdata.co/ regarding provided IP and save details into DB
    """)
def task(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        current_user = Authorize.get_jwt_subject()
        task = create_task.delay(current_user)
        return {"task_id": task.id}
    except Exception:
        raise HTTPException(status_code=500, detail="Task failed to create")


@router.get("/status/{id}", description="Show the result of the task")
def status(id: int, Authorize: AuthJWT = Depends()):
    return get_status_of_task(id)

