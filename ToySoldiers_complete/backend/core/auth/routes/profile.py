from fastapi import APIRouter, HTTPException, status, Header
from pydantic import BaseModel, EmailStr
from typing import Optional
from main import supabase
import uuid

router = APIRouter()

class ProfileResponse(BaseModel):
    id: uuid.UUID
    email: EmailStr
    role: str
    created_at: str
    creator_profile: Optional[dict] = None

class ProfileUpdateRequest(BaseModel):
    email: Optional[EmailStr] = None

async def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header"
        )
    
    try:
        token = authorization.replace("Bearer ", "")
        user_response = supabase.auth.get_user(token)
        
        if not user_response.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )
        
        return user_response.user
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}"
        )

@router.get("/profile", response_model=ProfileResponse)
async def get_profile(authorization: str = Header(None)):
    user = await get_current_user(authorization)
    
    user_data = supabase.table("users").select("*").eq("id", user.id).execute()
    
    if not user_data.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found"
        )
    
    profile = user_data.data[0]
    
    if profile["role"] == "creator":
        creator_data = supabase.table("creators").select("*").eq("user_id", user.id).execute()
        if creator_data.data:
            profile["creator_profile"] = creator_data.data[0]
    
    return ProfileResponse(**profile)

@router.patch("/profile")
async def update_profile(
    request: ProfileUpdateRequest,
    authorization: str = Header(None)
):
    user = await get_current_user(authorization)
    
    update_data = {}
    if request.email:
        update_data["email"] = request.email
    
    if update_data:
        supabase.table("users").update(update_data).eq("id", user.id).execute()
    
    return {"message": "Profile updated successfully"}

@router.delete("/profile")
async def delete_profile(authorization: str = Header(None)):
    user = await get_current_user(authorization)
    
    supabase.table("users").delete().eq("id", user.id).execute()
    
    return {"message": "Profile deleted successfully"}
