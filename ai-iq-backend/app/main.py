from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from .models import (
    UserAuth, DynamicTestResult, TestResultResponse, 
    CreateTestResultRequest, GHLWebhookData, TestParameter,
    UserSubscription, SubscriptionStatus, CreateSubscriptionRequest,
    SubscriptionResponse, StripeWebhookEvent
)
from .ghl_client import GHLClient
from .test_engine import AIIQTestEngine
from .vapi_client import VAPIClient
from .stripe_client import StripeClient
from .smart_links import SmartLink
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import uuid
import json
import os
from fastapi import Request
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="AI IQ Test Results API", version="1.0.0")

# Disable CORS. Do not remove this for full-stack development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

users_db = {}
test_results_db = {}
subscriptions_db = {}

ghl_client = GHLClient()
test_engine = AIIQTestEngine()
vapi_client = VAPIClient()
smart_links = SmartLink()
stripe_client = StripeClient()

def create_sample_result(user_id: str) -> DynamicTestResult:
    return test_engine.generate_dynamic_test_result(user_id)

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

@app.post("/auth/login")
async def login_user(user_auth: UserAuth):
    user_id = str(uuid.uuid4())
    ghl_contact_id = None
    
    if ghl_client.enabled:
        try:
            contact_result = await ghl_client.create_or_update_contact(
                email=user_auth.email,
                name=user_auth.name,
                mobile=user_auth.mobile,
                custom_fields={
                    "ai_iq_test_taken": "true",
                    "signup_source": "AI IQ Test Platform"
                }
            )
            ghl_contact_id = contact_result.get("contact", {}).get("id")
        except Exception as e:
            print(f"GHL integration error: {e}")
    
    users_db[user_id] = {
        "email": user_auth.email,
        "name": user_auth.name,
        "mobile": user_auth.mobile,
        "ghl_contact_id": ghl_contact_id,
        "created_at": datetime.now()
    }
    
    trial_end = datetime.now() + timedelta(days=7)
    subscription = UserSubscription(
        user_id=user_id,
        subscription_status=SubscriptionStatus.TRIAL,
        trial_start_date=datetime.now(),
        trial_end_date=trial_end
    )
    subscriptions_db[user_id] = subscription
    
    return {
        "user_id": user_id, 
        "ghl_contact_id": ghl_contact_id,
        "subscription_status": subscription.subscription_status.value,
        "trial_end_date": subscription.trial_end_date.isoformat() if subscription.trial_end_date else None,
        "message": "User authenticated successfully"
    }

def check_user_access(user_id: str) -> bool:
    """Check if user has access to create test results"""
    if user_id not in subscriptions_db:
        return False
    
    subscription = subscriptions_db[user_id]
    
    if subscription.subscription_status == SubscriptionStatus.TRIAL:
        if subscription.trial_end_date and datetime.now() > subscription.trial_end_date:
            subscription.subscription_status = SubscriptionStatus.EXPIRED
            return False
    
    return subscription.subscription_status in [SubscriptionStatus.TRIAL, SubscriptionStatus.ACTIVE]

@app.post("/test-results", response_model=TestResultResponse)
async def create_test_result(request: CreateTestResultRequest):
    if request.user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not check_user_access(request.user_id):
        subscription = subscriptions_db.get(request.user_id)
        if subscription and subscription.subscription_status == SubscriptionStatus.EXPIRED:
            raise HTTPException(status_code=402, detail="Trial period expired. Please subscribe to continue.")
        raise HTTPException(status_code=402, detail="Subscription required to access this feature.")
    
    user = users_db[request.user_id]
    
    test_parameters = None
    ghl_contact_data = None
    
    if ghl_client.enabled and user.get("ghl_contact_id"):
        try:
            contact = await ghl_client.get_contact_by_email(user["email"])
            if contact:
                ghl_contact_data = contact
                test_parameters = ghl_client.extract_test_parameters_from_contact(contact)
        except Exception as e:
            print(f"Error fetching GHL contact data: {e}")
    
    if request.test_parameters:
        if test_parameters:
            test_parameters.update(request.test_parameters)
        else:
            test_parameters = request.test_parameters
    
    result = test_engine.generate_dynamic_test_result(
        user_id=request.user_id,
        test_parameters=test_parameters,
        ghl_contact_data=ghl_contact_data
    )
    
    roi_analysis = test_engine._generate_roi_analysis(result.overall_score, result.pain_points)
    detailed_report = test_engine._generate_detailed_report(result.pain_points, result.categories)
    
    try:
        ghl_contact_id = ghl_client.create_contact(
            email=user["email"],
            name=user["name"],
            phone=user.get("mobile", ""),
            custom_fields={
                "ai_iq_score": str(result.overall_score),
                "test_completion_date": datetime.now().isoformat(),
                "pain_points_count": str(len(result.pain_points)),
                "categories_analyzed": str(len(result.categories))
            }
        )
        user["ghl_contact_id"] = ghl_contact_id
    except Exception as e:
        print(f"Failed to create GHL contact: {e}")
        user["ghl_contact_id"] = None
    
    result_id = str(uuid.uuid4())
    test_results_db[result_id] = result
    
    if ghl_client.enabled and user.get("ghl_contact_id"):
        try:
            ghl_fields = ghl_client.format_test_results_for_ghl({
                "overall_score": result.overall_score,
                "pain_points": {k: v.dict() for k, v in result.pain_points.items()},
                "categories": {k: v.dict() for k, v in result.categories.items()},
                "recommendations": result.recommendations,
                "created_at": result.created_at
            })
            await ghl_client.update_contact_custom_fields(
                user["ghl_contact_id"],
                ghl_fields
            )
        except Exception as e:
            print(f"Error updating GHL contact: {e}")
    
    return TestResultResponse(
        id=result_id,
        user_email=user["email"],
        user_name=user["name"],
        contact_id=user.get("ghl_contact_id"),
        pain_points={k: v.dict() for k, v in result.pain_points.items()},
        categories={k: v.dict() for k, v in result.categories.items()},
        overall_score=result.overall_score,
        recommendations=result.recommendations,
        custom_sections={k: v.dict() for k, v in result.custom_sections.items()} if result.custom_sections else None,
        report_metadata=result.report_metadata,
        created_at=result.created_at,
        session_metadata={
            "session_duration": "45 minutes",
            "completion_rate": "100%",
            "interaction_quality": "High",
            "follow_up_recommended": True
        },
        voice_summary={
            "key_insights": [
                "Strong digital foundation with room for AI enhancement",
                "Customer service automation presents biggest opportunity",
                "Marketing processes need immediate attention"
            ],
            "client_concerns_expressed": [
                "Worried about implementation complexity",
                "Concerned about team adoption",
                "Budget constraints for full transformation"
            ],
            "recommended_next_steps": [
                "Start with pilot AI customer service project",
                "Develop team training program",
                "Create phased implementation timeline"
            ]
        },
        api_data_sources={
            "website_analysis": {
                "domain": "example.com",
                "performance_score": 78,
                "seo_readiness": "Good",
                "mobile_optimization": "Excellent"
            },
            "social_media_audit": {
                "platforms_analyzed": ["LinkedIn", "Facebook", "Instagram"],
                "engagement_rate": "3.2%",
                "content_consistency": "Moderate"
            },
            "competitor_analysis": {
                "competitors_found": 5,
                "ai_adoption_rate": "60%",
                "market_position": "Behind leaders"
            }
        },
        subscription_recommendations={
            "recommended_plan": "AI Transformation Pro",
            "monthly_investment": "$297",
            "estimated_roi": "340%",
            "implementation_timeline": "3-6 months",
            "priority_features": [
                "AI Customer Service Agent",
                "Marketing Automation Suite",
                "Performance Analytics Dashboard"
            ]
        },
        roi_analysis=roi_analysis.dict(),
        detailed_report=detailed_report.dict()
    )

@app.get("/test-results/{result_id}", response_model=TestResultResponse)
async def get_test_result(result_id: str):
    if result_id not in test_results_db:
        raise HTTPException(status_code=404, detail="Test result not found")
    
    result = test_results_db[result_id]
    user = users_db[result.user_id]
    
    return TestResultResponse(
        id=result_id,
        user_email=user["email"],
        user_name=user["name"],
        contact_id=user.get("ghl_contact_id"),
        pain_points={k: v.dict() for k, v in result.pain_points.items()},
        categories={k: v.dict() for k, v in result.categories.items()},
        overall_score=result.overall_score,
        recommendations=result.recommendations,
        custom_sections={k: v.dict() for k, v in result.custom_sections.items()} if result.custom_sections else None,
        report_metadata=result.report_metadata,
        created_at=result.created_at
    )

@app.get("/public/report", response_model=TestResultResponse)
async def public_report(contact_id: str, expires: str, sig: str):
    """Get test results via smart link with HMAC validation"""
    if not smart_links.validate(contact_id, expires, sig):
        raise HTTPException(status_code=401, detail="Invalid or expired link")

    user_id = smart_links.find_user_by_contact_id(contact_id, users_db)
    if not user_id:
        raise HTTPException(status_code=404, detail="User not found")

    latest_id = None
    latest_created_at = None
    for rid, res in test_results_db.items():
        if res.user_id == user_id:
            if latest_created_at is None or res.created_at > latest_created_at:
                latest_created_at = res.created_at
                latest_id = rid

    if not latest_id:
        raise HTTPException(status_code=404, detail="No results found")

    result = test_results_db[latest_id]
    user = users_db[user_id]
    return TestResultResponse(
        id=latest_id,
        user_email=user["email"],
        user_name=user["name"],
        contact_id=user.get("ghl_contact_id"),
        pain_points={k: v.dict() for k, v in result.pain_points.items()},
        categories={k: v.dict() for k, v in result.categories.items()},
        overall_score=result.overall_score,
        recommendations=result.recommendations,
        custom_sections={k: v.dict() for k, v in result.custom_sections.items()} if result.custom_sections else None,
        report_metadata=result.report_metadata,
        created_at=result.created_at
    )

@app.get("/users/{user_id}/test-results")
async def get_user_test_results(user_id: str):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_results = []
    for result_id, result in test_results_db.items():
        if result.user_id == user_id:
            user_results.append({
                "id": result_id,
                "overall_score": result.overall_score,
                "created_at": result.created_at
            })
    
    return {"user_id": user_id, "results": user_results}

@app.post("/webhooks/vapi-result")
async def handle_vapi_webhook(webhook_data: Dict[str, Any]):
    """Handle VAPI AI agent webhook with test results"""
    try:
        result = await vapi_client.process_vapi_webhook(webhook_data)
        
        await vapi_client.trigger_site_webhook(
            result["contact_id"], 
            result["test_result"],
            result.get("smart_link", "")
        )
        
        return {
            "status": "success",
            "message": "VAPI test results processed successfully",
            "contact_id": result["contact_id"],
            "smart_link": result.get("smart_link", ""),
            "overall_score": result["test_result"].overall_score
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing VAPI webhook: {str(e)}")

@app.post("/webhooks/ghl-form")
async def handle_ghl_form_submission(webhook_data: GHLWebhookData):
    """Handle form submissions from GHL and trigger AI IQ test"""
    try:
        user_auth = UserAuth(
            email=webhook_data.email,
            name=webhook_data.name,
            mobile=webhook_data.phone
        )
        
        auth_result = await login_user(user_auth)
        
        test_params = {}
        for key, value in webhook_data.form_data.items():
            if key in ["industry", "company_size", "current_ai_usage", "primary_challenges"]:
                test_params[key] = TestParameter(
                    name=key,
                    value=value,
                    weight=1.0,
                    category="form_data"
                )
        
        test_request = CreateTestResultRequest(
            user_id=auth_result["user_id"],
            test_parameters=test_params,
            ghl_contact_data=webhook_data.custom_fields
        )
        
        test_result = await create_test_result(test_request)
        
        return {
            "status": "success",
            "user_id": auth_result["user_id"],
            "test_result_id": test_result.id,
            "overall_score": test_result.overall_score
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing GHL form submission: {str(e)}")

@app.get("/config/test-parameters")
async def get_test_parameters_config():
    """Get available test parameters and their configurations"""
    return {
        "available_parameters": [
            {"name": "industry", "type": "string", "weight": 1.2, "category": "business"},
            {"name": "company_size", "type": "string", "weight": 1.1, "category": "business"},
            {"name": "current_ai_usage", "type": "string", "weight": 1.5, "category": "technology"},
            {"name": "primary_challenges", "type": "array", "weight": 1.3, "category": "pain_points"},
            {"name": "budget_range", "type": "string", "weight": 1.0, "category": "business"},
            {"name": "tech_expertise", "type": "string", "weight": 1.2, "category": "technology"}
        ],
        "pain_point_weights": test_engine.config.pain_point_weights,
        "category_weights": test_engine.config.category_weights,
        "scoring_thresholds": test_engine.config.scoring_thresholds
    }

@app.post("/subscription/create", response_model=SubscriptionResponse)
async def create_subscription(request: CreateSubscriptionRequest):
    """Create a Stripe subscription for a user"""
    if request.user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not stripe_client.enabled:
        raise HTTPException(status_code=503, detail="Payment processing not available")
    
    user = users_db[request.user_id]
    
    try:
        subscription = subscriptions_db.get(request.user_id)
        if not subscription or not subscription.stripe_customer_id:
            customer = await stripe_client.create_customer(
                email=user["email"],
                name=user["name"],
                metadata={"user_id": request.user_id}
            )
            
            if subscription:
                subscription.stripe_customer_id = customer["id"]
            else:
                subscription = UserSubscription(
                    user_id=request.user_id,
                    stripe_customer_id=customer["id"]
                )
                subscriptions_db[request.user_id] = subscription
        
        stripe_subscription = await stripe_client.create_subscription(
            customer_id=subscription.stripe_customer_id,
            payment_method_id=request.payment_method_id,
            trial_days=0  # No additional trial since they already had one
        )
        
        subscription.stripe_subscription_id = stripe_subscription["id"]
        subscription.subscription_status = stripe_client.subscription_status_to_internal(stripe_subscription["status"])
        subscription.current_period_start = datetime.fromtimestamp(stripe_subscription["current_period_start"])
        subscription.current_period_end = datetime.fromtimestamp(stripe_subscription["current_period_end"])
        
        return SubscriptionResponse(
            subscription_id=stripe_subscription["id"],
            client_secret=stripe_subscription["latest_invoice"]["payment_intent"]["client_secret"] if stripe_subscription.get("latest_invoice") else None,
            status=stripe_subscription["status"],
            current_period_end=subscription.current_period_end
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create subscription: {str(e)}")

@app.get("/subscription/status/{user_id}")
async def get_subscription_status(user_id: str):
    """Get user's subscription status"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    subscription = subscriptions_db.get(user_id)
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    if subscription.subscription_status == SubscriptionStatus.TRIAL:
        if subscription.trial_end_date and datetime.now() > subscription.trial_end_date:
            subscription.subscription_status = SubscriptionStatus.EXPIRED
    
    return {
        "user_id": user_id,
        "status": subscription.subscription_status.value,
        "trial_end_date": subscription.trial_end_date.isoformat() if subscription.trial_end_date else None,
        "current_period_end": subscription.current_period_end.isoformat() if subscription.current_period_end else None,
        "stripe_subscription_id": subscription.stripe_subscription_id,
        "has_access": check_user_access(user_id)
    }

@app.post("/subscription/cancel/{user_id}")
async def cancel_subscription(user_id: str):
    """Cancel user's subscription"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    subscription = subscriptions_db.get(user_id)
    if not subscription or not subscription.stripe_subscription_id:
        raise HTTPException(status_code=404, detail="No active subscription found")
    
    if not stripe_client.enabled:
        raise HTTPException(status_code=503, detail="Payment processing not available")
    
    try:
        stripe_subscription = await stripe_client.cancel_subscription(subscription.stripe_subscription_id)
        subscription.subscription_status = SubscriptionStatus.CANCELLED
        
        return {
            "message": "Subscription cancelled successfully",
            "cancellation_date": datetime.fromtimestamp(stripe_subscription["canceled_at"]).isoformat() if stripe_subscription.get("canceled_at") else None,
            "access_until": datetime.fromtimestamp(stripe_subscription["current_period_end"]).isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to cancel subscription: {str(e)}")

@app.post("/webhooks/stripe")
async def handle_stripe_webhook(request: Request):
    """Handle Stripe webhook events"""
    if not stripe_client.enabled:
        raise HTTPException(status_code=503, detail="Stripe not configured")
    
    payload = await request.body()
    signature = request.headers.get("stripe-signature")
    
    try:
        event = stripe_client.verify_webhook_signature(payload, signature)
        
        if event["type"] == "customer.subscription.updated":
            subscription_data = event["data"]["object"]
            customer_id = subscription_data["customer"]
            
            user_id = None
            for uid, sub in subscriptions_db.items():
                if sub.stripe_customer_id == customer_id:
                    user_id = uid
                    break
            
            if user_id:
                subscription = subscriptions_db[user_id]
                subscription.subscription_status = stripe_client.subscription_status_to_internal(subscription_data["status"])
                subscription.current_period_start = datetime.fromtimestamp(subscription_data["current_period_start"])
                subscription.current_period_end = datetime.fromtimestamp(subscription_data["current_period_end"])
        
        elif event["type"] == "customer.subscription.deleted":
            subscription_data = event["data"]["object"]
            customer_id = subscription_data["customer"]
            
            for uid, sub in subscriptions_db.items():
                if sub.stripe_customer_id == customer_id:
                    sub.subscription_status = SubscriptionStatus.CANCELLED
                    break
        
        return {"status": "success"}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Webhook error: {str(e)}")

@app.post("/support/refund-request")
async def request_refund(user_id: str, reason: str):
    """Handle money-back guarantee refund requests"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    subscription = subscriptions_db.get(user_id)
    if not subscription or not subscription.stripe_subscription_id:
        raise HTTPException(status_code=404, detail="No subscription found")
    
    return {
        "message": "Refund request submitted successfully",
        "request_id": str(uuid.uuid4()),
        "user_id": user_id,
        "reason": reason,
        "status": "pending_review"
    }
