import stripe
import os
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from .models import UserSubscription, SubscriptionStatus

class StripeClient:
    def __init__(self):
        self.api_key = os.getenv("STRIPE_SECRET_KEY")
        self.webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
        self.enabled = bool(self.api_key)
        
        if self.enabled:
            stripe.api_key = self.api_key
    
    async def create_customer(self, email: str, name: str, metadata: Dict[str, str] = None) -> Dict[str, Any]:
        """Create a new Stripe customer"""
        if not self.enabled:
            raise Exception("Stripe not configured")
        
        customer_data = {
            "email": email,
            "name": name,
            "metadata": metadata or {}
        }
        
        customer = stripe.Customer.create(**customer_data)
        return customer
    
    async def create_subscription(self, customer_id: str, payment_method_id: str, trial_days: int = 7) -> Dict[str, Any]:
        """Create a subscription with trial period"""
        if not self.enabled:
            raise Exception("Stripe not configured")
        
        stripe.PaymentMethod.attach(
            payment_method_id,
            customer=customer_id,
        )
        
        stripe.Customer.modify(
            customer_id,
            invoice_settings={
                'default_payment_method': payment_method_id,
            },
        )
        
        subscription = stripe.Subscription.create(
            customer=customer_id,
            items=[{
                'price': os.getenv("STRIPE_PRICE_ID", "price_1234567890"),  # $100/month price ID
            }],
            trial_period_days=trial_days,
            payment_behavior='default_incomplete',
            payment_settings={'save_default_payment_method': 'on_subscription'},
            expand=['latest_invoice.payment_intent'],
        )
        
        return subscription
    
    async def cancel_subscription(self, subscription_id: str) -> Dict[str, Any]:
        """Cancel a subscription"""
        if not self.enabled:
            raise Exception("Stripe not configured")
        
        subscription = stripe.Subscription.modify(
            subscription_id,
            cancel_at_period_end=True
        )
        return subscription
    
    async def get_subscription(self, subscription_id: str) -> Dict[str, Any]:
        """Get subscription details"""
        if not self.enabled:
            raise Exception("Stripe not configured")
        
        subscription = stripe.Subscription.retrieve(subscription_id)
        return subscription
    
    async def process_refund(self, payment_intent_id: str, amount: Optional[int] = None) -> Dict[str, Any]:
        """Process a refund for money-back guarantee"""
        if not self.enabled:
            raise Exception("Stripe not configured")
        
        refund_data = {"payment_intent": payment_intent_id}
        if amount:
            refund_data["amount"] = amount
        
        refund = stripe.Refund.create(**refund_data)
        return refund
    
    def verify_webhook_signature(self, payload: bytes, signature: str) -> Dict[str, Any]:
        """Verify webhook signature and return event"""
        if not self.enabled or not self.webhook_secret:
            raise Exception("Stripe webhook not configured")
        
        try:
            event = stripe.Webhook.construct_event(
                payload, signature, self.webhook_secret
            )
            return event
        except ValueError:
            raise Exception("Invalid payload")
        except stripe.error.SignatureVerificationError:
            raise Exception("Invalid signature")
    
    def subscription_status_to_internal(self, stripe_status: str) -> SubscriptionStatus:
        """Convert Stripe subscription status to internal status"""
        status_mapping = {
            "trialing": SubscriptionStatus.TRIAL,
            "active": SubscriptionStatus.ACTIVE,
            "canceled": SubscriptionStatus.CANCELLED,
            "incomplete_expired": SubscriptionStatus.EXPIRED,
            "past_due": SubscriptionStatus.PAST_DUE,
            "unpaid": SubscriptionStatus.PAST_DUE,
        }
        return status_mapping.get(stripe_status, SubscriptionStatus.EXPIRED)
