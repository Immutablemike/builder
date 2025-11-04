from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from main import supabase
from models.content import ContentResponse

router = APIRouter()

@router.get("/feed", response_model=List[ContentResponse])
async def get_feed(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    visibility: Optional[str] = "public",
    tags: Optional[str] = None
):
    try:
        query = supabase.table("content").select("*").eq("visibility", visibility)
        
        if tags:
            tags_list = tags.split(',')
            query = query.contains("tags", tags_list)
        
        content_data = query.order("created_at", desc=True).limit(limit).offset(offset).execute()
        
        return [ContentResponse(**item) for item in content_data.data]
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get feed: {str(e)}"
        )

@router.get("/creator/{creator_id}", response_model=List[ContentResponse])
async def get_creator_content(
    creator_id: str,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    try:
        content_data = supabase.table("content") \
            .select("*") \
            .eq("creator_id", creator_id) \
            .eq("visibility", "public") \
            .order("created_at", desc=True) \
            .limit(limit) \
            .offset(offset) \
            .execute()
        
        return [ContentResponse(**item) for item in content_data.data]
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get creator content: {str(e)}"
        )

@router.get("/search")
async def search_content(
    q: str = Query(..., min_length=1),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    try:
        content_data = supabase.table("content") \
            .select("*") \
            .or_(f"title.ilike.%{q}%,description.ilike.%{q}%") \
            .eq("visibility", "public") \
            .order("created_at", desc=True) \
            .limit(limit) \
            .offset(offset) \
            .execute()
        
        return {
            "results": [ContentResponse(**item) for item in content_data.data],
            "total": len(content_data.data),
            "query": q
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Search failed: {str(e)}"
        )
