from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import Optional
from main import supabase
from datetime import datetime

router = APIRouter()

class ViewEvent(BaseModel):
    content_id: str
    duration: Optional[float] = None
    device_type: Optional[str] = None
    referrer: Optional[str] = None

@router.post("/analytics/view")
async def track_view(
    event: ViewEvent,
    authorization: str = Header(None)
):
    try:
        user_id = None
        if authorization:
            token = authorization.replace("Bearer ", "")
            user_response = supabase.auth.get_user(token)
            if user_response.user:
                user_id = str(user_response.user.id)
        
        view_data = {
            "date": datetime.utcnow().date().isoformat(),
            "user_id": user_id,
            "content_id": event.content_id,
            "view_count": 1,
            "duration": event.duration,
            "device_type": event.device_type,
            "referrer": event.referrer
        }
        
        supabase.table("analytics_views").insert(view_data).execute()
        
        return {"status": "success", "message": "View tracked"}
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to track view: {str(e)}"
        )

@router.get("/analytics/content/{content_id}")
async def get_content_analytics(
    content_id: str,
    authorization: str = Header(None)
):
    try:
        if not authorization:
            raise HTTPException(
                status_code=401,
                detail="Authentication required"
            )
        
        views_data = supabase.table("analytics_views") \
            .select("*") \
            .eq("content_id", content_id) \
            .execute()
        
        total_views = len(views_data.data)
        total_duration = sum(v.get("duration", 0) or 0 for v in views_data.data)
        
        return {
            "content_id": content_id,
            "total_views": total_views,
            "total_watch_time": total_duration,
            "average_watch_time": total_duration / total_views if total_views > 0 else 0
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get analytics: {str(e)}"
        )
