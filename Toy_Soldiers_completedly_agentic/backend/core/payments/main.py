from fastapi import FastAPI, HTTPException, Depends, Request
from pydantic import BaseModel
import stripe
import os
import uvicorn
from typing import Optional

# Configuration
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

app = FastAPI(title="ToySoldiers Payment Service", version="1.0.0")

# Pydantic models
class TipRequest(BaseModel):
    amount: int  # Amount in cents
    creator_id: int
    fan_id: int
    message: Optional[str] = None

class SubscriptionRequest(BaseModel):
    creator_id: int
    fan_id: int
    price_id: str

class PaymentResponse(BaseModel):
    payment_intent_id: str
    client_secret: str
    status: str

# Routes
@app.post("/create-tip", response_model=PaymentResponse)
async def create_tip(tip_request: TipRequest):
    try:
        intent = stripe.PaymentIntent.create(
            amount=tip_request.amount,
            currency='usd',
            metadata={
                'type': 'tip',
                'creator_id': tip_request.creator_id,
                'fan_id': tip_request.fan_id,
                'message': tip_request.message or ''
            }
        )
        
        return PaymentResponse(
            payment_intent_id=intent.id,
            client_secret=intent.client_secret,
            status=intent.status
        )
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/create-subscription", response_model=dict)
async def create_subscription(sub_request: SubscriptionRequest):
    try:
        subscription = stripe.Subscription.create(
            customer=f"fan_{sub_request.fan_id}",
            items=[{
                'price': sub_request.price_id,
            }],
            metadata={
                'creator_id': sub_request.creator_id,
                'fan_id': sub_request.fan_id
            }
        )
        
        return {
            "subscription_id": subscription.id,
            "status": subscription.status,
            "current_period_end": subscription.current_period_end
        }
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        # Process successful payment
        print(f"Payment succeeded: {payment_intent['id']}")
    
    elif event['type'] == 'customer.subscription.created':
        subscription = event['data']['object']
        # Handle new subscription
        print(f"Subscription created: {subscription['id']}")
    
    return {"status": "success"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "payments"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)