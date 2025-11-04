from fastapi import APIRouter, HTTPException, status, Header
from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
import stripe
from main import supabase
import uuid

router = APIRouter()

class CheckoutRequest(BaseModel):
    to_creator_id: str
    amount: float
    currency: str = "usd"
    success_url: str
    cancel_url: str

class CheckoutResponse(BaseModel):
    checkout_url: str
    session_id: str

@router.post("/checkout", response_model=CheckoutResponse)
async def create_checkout_session(
    request: CheckoutRequest,
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
        
        creator_data = supabase.table("creators").select("*").eq("id", request.to_creator_id).execute()
        
        if not creator_data.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Creator not found"
            )
        
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': request.currency,
                    'unit_amount': int(request.amount * 100),
                    'product_data': {
                        'name': 'Tip to Creator',
                    },
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.success_url,
            cancel_url=request.cancel_url,
            metadata={
                'from_user_id': str(user_response.user.id),
                'to_creator_id': request.to_creator_id,
                'type': 'tip'
            }
        )
        
        tip_data = {
            "from_user": str(user_response.user.id),
            "to_creator": request.to_creator_id,
            "amount": request.amount,
            "stripe_txn": session.id,
            "status": "pending"
        }
        supabase.table("tips").insert(tip_data).execute()
        
        return CheckoutResponse(
            checkout_url=session.url,
            session_id=session.id
        )
        
    except stripe.error.StripeError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Stripe error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Checkout failed: {str(e)}"
        )

@router.post("/tip")
async def create_tip(
    to_creator_id: str,
    amount: float,
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
        
        payment_intent = stripe.PaymentIntent.create(
            amount=int(amount * 100),
            currency='usd',
            metadata={
                'from_user_id': str(user_response.user.id),
                'to_creator_id': to_creator_id
            }
        )
        
        return {
            "client_secret": payment_intent.client_secret,
            "payment_intent_id": payment_intent.id
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Tip creation failed: {str(e)}"
        )

@router.get("/history")
async def get_payment_history(
    authorization: str = Header(None),
    limit: int = 50,
    offset: int = 0
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
        
        tips_data = supabase.table("tips") \
            .select("*") \
            .eq("from_user", str(user_response.user.id)) \
            .order("created_at", desc=True) \
            .limit(limit) \
            .offset(offset) \
            .execute()
        
        return {
            "tips": tips_data.data,
            "total": len(tips_data.data)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get payment history: {str(e)}"
        )
