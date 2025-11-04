from fastapi import APIRouter, HTTPException
from main import supabase

router = APIRouter()

@router.get("/stream/{content_id}")
async def get_stream_url(content_id: str):
    try:
        content_data = supabase.table("content").select("*").eq("id", content_id).execute()
        
        if not content_data.data:
            raise HTTPException(
                status_code=404,
                detail="Content not found"
            )
        
        content = content_data.data[0]
        
        if content["visibility"] == "private":
            raise HTTPException(
                status_code=403,
                detail="Content is private"
            )
        
        return {
            "content_id": content_id,
            "stream_url": content.get("stream_url") or content.get("media_url"),
            "title": content["title"],
            "duration": content.get("duration")
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get stream URL: {str(e)}"
        )
