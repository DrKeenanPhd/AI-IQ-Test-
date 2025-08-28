from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from .models import (
    UserAuth, DynamicTestResult, TestResultResponse, 
    CreateTestResultRequest, GHLWebhookData, TestParameter
)
from .ghl_client import GHLClient
from .test_engine import AIIQTestEngine
from typing import Dict, List, Optional, Any
from datetime import datetime
import uuid
import json
import os

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

ghl_client = GHLClient()
test_engine = AIIQTestEngine()

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
    
    return {
        "user_id": user_id, 
        "ghl_contact_id": ghl_contact_id,
        "message": "User authenticated successfully"
    }

@app.post("/test-results", response_model=TestResultResponse)
async def create_test_result(request: CreateTestResultRequest):
    if request.user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
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
        pain_points={k: v.dict() for k, v in result.pain_points.items()},
        categories={k: v.dict() for k, v in result.categories.items()},
        overall_score=result.overall_score,
        recommendations=result.recommendations,
        custom_sections={k: v.dict() for k, v in result.custom_sections.items()} if result.custom_sections else None,
        report_metadata=result.report_metadata,
        created_at=result.created_at
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
