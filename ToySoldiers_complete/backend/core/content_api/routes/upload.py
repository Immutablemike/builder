from fastapi import APIRouter, HTTPException, status, Header, UploadFile, File, Form
from typing import Optional
import uuid
from main import supabase, r2_client, settings
from models.content import ContentCreate, ContentResponse

router = APIRouter()

@router.post("/upload", response_model=ContentResponse, status_code=status.HTTP_201_CREATED)
async def upload_content(
    file: UploadFile = File(...),
    title: str = Form(...),
    description: Optional[str] = Form(None),
    tags: Optional[str] = Form(None),
    visibility: str = Form("public"),
    authorization: str = Header(None)
):
    try:
        if not authorization:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required"
            )
        
        token = authorization.replace("Bearer ", "")
        user_response = supabase.auth.get_user(token)
        
        if not user_response.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        creator_data = supabase.table("creators").select("*").eq("user_id", str(user_response.user.id)).execute()
        
        if not creator_data.data:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not a creator account"
            )
        
        creator_id = creator_data.data[0]["id"]
        content_id = str(uuid.uuid4())
        file_extension = file.filename.split('.')[-1]
        
        file_content = await file.read()
        
        bucket = settings.r2_bucket_video if file.content_type.startswith('video') else settings.r2_bucket_audio
        
        object_key = f"{creator_id}/{content_id}.{file_extension}"
        
        r2_client.put_object(
            Bucket=bucket,
            Key=object_key,
            Body=file_content,
            ContentType=file.content_type
        )
        
        media_url = f"https://{settings.cloudflare_account_id}.r2.cloudflarestorage.com/{bucket}/{object_key}"
        
        tags_list = tags.split(',') if tags else []
        
        content_data = {
            "id": content_id,
            "creator_id": creator_id,
            "title": title,
            "description": description,
            "media_url": media_url,
            "tags": tags_list,
            "visibility": visibility,
            "file_size": len(file_content)
        }
        
        result = supabase.table("content").insert(content_data).execute()
        
        return ContentResponse(**result.data[0])
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Upload failed: {str(e)}"
        )

@router.get("/{content_id}", response_model=ContentResponse)
async def get_content(content_id: str):
    try:
        content_data = supabase.table("content").select("*").eq("id", content_id).execute()
        
        if not content_data.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Content not found"
            )
        
        return ContentResponse(**content_data.data[0])
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get content: {str(e)}"
        )

@router.delete("/{content_id}")
async def delete_content(
    content_id: str,
    authorization: str = Header(None)
):
    try:
        if not authorization:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required"
            )
        
        token = authorization.replace("Bearer ", "")
        user_response = supabase.auth.get_user(token)
        
        if not user_response.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        content_data = supabase.table("content").select("*").eq("id", content_id).execute()
        
        if not content_data.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Content not found"
            )
        
        creator_data = supabase.table("creators").select("*").eq("user_id", str(user_response.user.id)).execute()
        
        if not creator_data.data or content_data.data[0]["creator_id"] != creator_data.data[0]["id"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this content"
            )
        
        supabase.table("content").delete().eq("id", content_id).execute()
        
        return {"message": "Content deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete content: {str(e)}"
        )
