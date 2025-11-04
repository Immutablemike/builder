from fastapi import APIRouter, Request, HTTPException, status
import stripe
from main import settings, supabase

router = APIRouter()

@router.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.stripe_webhook_secret
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        from_user_id = session['metadata'].get('from_user_id')
        to_creator_id = session['metadata'].get('to_creator_id')
        
        supabase.table("tips").update({
            "status": "completed"
        }).eq("stripe_txn", session['id']).execute()
        
    elif event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        
        from_user_id = payment_intent['metadata'].get('from_user_id')
        to_creator_id = payment_intent['metadata'].get('to_creator_id')
        
        tip_data = {
            "from_user": from_user_id,
            "to_creator": to_creator_id,
            "amount": payment_intent['amount'] / 100,
            "stripe_txn": payment_intent['id'],
            "status": "completed"
        }
        supabase.table("tips").insert(tip_data).execute()
        
    elif event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
        
        supabase.table("tips").update({
            "status": "failed"
        }).eq("stripe_txn", payment_intent['id']).execute()
    
    return {"status": "success"}
