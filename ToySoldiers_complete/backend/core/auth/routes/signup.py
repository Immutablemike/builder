from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from main import supabase, posthog_client
from models.user import UserCreate, UserResponse
import uuid

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    role: str = "fan"

class SignupResponse(BaseModel):
    user: UserResponse
    message: str

@router.post("/signup", response_model=SignupResponse, status_code=status.HTTP_201_CREATED)
async def signup(request: SignupRequest):
    try:
        auth_response = supabase.auth.sign_up({
            "email": request.email,
            "password": request.password,
            "options": {
                "data": {
                    "role": request.role
                }
            }
        })
        
        if not auth_response.user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create user account"
            )
        
        user_data = {
            "id": auth_response.user.id,
            "email": request.email,
            "role": request.role,
            "created_at": auth_response.user.created_at
        }
        
        supabase.table("users").insert({
            "id": auth_response.user.id,
            "email": request.email,
            "role": request.role
        }).execute()
        
        if request.role == "creator":
            supabase.table("creators").insert({
                "user_id": auth_response.user.id,
                "bio": "",
                "tiers": {},
                "verified": False
            }).execute()
        
        posthog_client.capture(
            str(auth_response.user.id),
            'user_signup',
            {
                'email': request.email,
                'role': request.role
            }
        )
        
        return SignupResponse(
            user=UserResponse(**user_data),
            message="Account created successfully. Please check your email to verify your account."
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Signup failed: {str(e)}"
        )
