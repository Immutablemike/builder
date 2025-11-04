from fastapi import APIRouter, HTTPException, status, Header
from pydantic import BaseModel
from typing import List
import stripe
from main import supabase
from datetime import datetime, timedelta

router = APIRouter()

class PayoutRequest(BaseModel):
    amount: float
    currency: str = "usd"

class PayoutResponse(BaseModel):
    payout_id: str
    amount: float
    status: str
    arrival_date: str

@router.get("/payouts")
async def get_payouts(
    authorization: str = Header(None),
    limit: int = 50
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
        
        tips_data = supabase.table("tips") \
            .select("*") \
            .eq("to_creator", creator_data.data[0]["id"]) \
            .eq("status", "completed") \
            .order("created_at", desc=True) \
            .limit(limit) \
            .execute()
        
        total_earnings = sum(tip["amount"] for tip in tips_data.data)
        
        return {
            "total_earnings": total_earnings,
            "tips": tips_data.data,
            "total_tips": len(tips_data.data)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get payouts: {str(e)}"
        )

@router.post("/payouts/request", response_model=PayoutResponse)
async def request_payout(
    request: PayoutRequest,
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
        
        payout_account = creator_data.data[0].get("payout_account")
        
        if not payout_account:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No payout account configured"
            )
        
        payout = stripe.Payout.create(
            amount=int(request.amount * 100),
            currency=request.currency,
            stripe_account=payout_account
        )
        
        arrival_date = datetime.utcnow() + timedelta(days=2)
        
        return PayoutResponse(
            payout_id=payout.id,
            amount=request.amount,
            status=payout.status,
            arrival_date=arrival_date.isoformat()
        )
        
    except stripe.error.StripeError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Stripe error: {str(e)}"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Payout request failed: {str(e)}"
        )
