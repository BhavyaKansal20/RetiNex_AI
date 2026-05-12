from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from jose import JWTError, jwt
import bcrypt
from backend.config import JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRY_HOURS
from backend.database import db

router = APIRouter(prefix="/api/auth", tags=["Authentication"])
security = HTTPBearer()


class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict


class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    created_at: str


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))


def create_token(user_id: str, username: str) -> str:
    payload = {
        "sub": user_id,
        "username": username,
        "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRY_HOURS),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = db.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user


@router.post("/register", response_model=TokenResponse)
def register(request: RegisterRequest):
    if db.get_user_by_email(request.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    if db.get_user_by_username(request.username):
        raise HTTPException(status_code=400, detail="Username already taken")
    if len(request.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")

    hashed = hash_password(request.password)
    user = db.create_user(request.username, request.email, hashed)

    token = create_token(user["id"], user["username"])
    return TokenResponse(
        access_token=token,
        user={"id": user["id"], "username": user["username"], "email": user["email"]},
    )


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest):
    user = db.get_user_by_email(request.email)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not verify_password(request.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token(user["id"], user["username"])
    return TokenResponse(
        access_token=token,
        user={"id": user["id"], "username": user["username"], "email": user["email"]},
    )


@router.get("/me")
def get_profile(user: dict = Depends(get_current_user)):
    return {
        "id": user["id"],
        "username": user["username"],
        "email": user["email"],
        "created_at": user.get("created_at", ""),
    }
