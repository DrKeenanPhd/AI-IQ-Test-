from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Dict, List, Optional, Any
from datetime import datetime
import uuid
import json

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

class UserAuth(BaseModel):
    email: EmailStr
    name: str
    mobile: str

class TestResult(BaseModel):
    user_id: str
    pain_points: Dict[str, Dict[str, Any]]
    categories: Dict[str, Dict[str, Any]]
    overall_score: int
    recommendations: List[str]
    created_at: datetime

class TestResultResponse(BaseModel):
    id: str
    user_email: str
    user_name: str
    pain_points: Dict[str, Dict[str, Any]]
    categories: Dict[str, Dict[str, Any]]
    overall_score: int
    recommendations: List[str]
    created_at: datetime

def create_sample_result(user_id: str) -> TestResult:
    return TestResult(
        user_id=user_id,
        pain_points={
            "cant_scale_without_burnout": {
                "score": 7,
                "description": "Struggling with delegation and automation",
                "severity": "high",
                "recommendations": ["Implement AI-powered task automation", "Create standard operating procedures"]
            },
            "invisible_attention_landscape": {
                "score": 5,
                "description": "Limited visibility in digital channels",
                "severity": "medium",
                "recommendations": ["Optimize SEO strategy", "Increase social media presence"]
            },
            "outgunned_by_competitors": {
                "score": 8,
                "description": "Competitors using advanced AI tools",
                "severity": "high",
                "recommendations": ["Adopt AI-powered analytics", "Implement chatbot solutions"]
            },
            "tech_gap_ai_advantages": {
                "score": 6,
                "description": "Underutilizing available AI technologies",
                "severity": "medium",
                "recommendations": ["AI training for team", "Implement AI workflow automation"]
            }
        },
        categories={
            "website_form_function": {
                "score": 32,
                "max_score": 40,
                "percentage": 80,
                "strengths": ["Good mobile responsiveness", "Fast loading times"],
                "weaknesses": ["Poor conversion optimization", "Limited AI integration"],
                "priority_actions": ["Add AI chatbot", "Implement dynamic personalization"]
            },
            "social_media_effectiveness": {
                "score": 28,
                "max_score": 40,
                "percentage": 70,
                "strengths": ["Consistent posting", "Good engagement rates"],
                "weaknesses": ["Limited automation", "No AI content generation"],
                "priority_actions": ["Implement AI content creation", "Automate posting schedules"]
            },
            "digital_presence": {
                "score": 30,
                "max_score": 40,
                "percentage": 75,
                "strengths": ["Strong brand recognition", "Good online reviews"],
                "weaknesses": ["Limited SEO optimization", "No AI-powered insights"],
                "priority_actions": ["AI-powered SEO optimization", "Implement analytics automation"]
            },
            "communication": {
                "score": 26,
                "max_score": 40,
                "percentage": 65,
                "strengths": ["Clear messaging", "Good customer service"],
                "weaknesses": ["Manual processes", "No AI assistance"],
                "priority_actions": ["Deploy AI customer service", "Automate follow-up sequences"]
            },
            "marketing": {
                "score": 34,
                "max_score": 40,
                "percentage": 85,
                "strengths": ["Good targeting", "Strong campaigns"],
                "weaknesses": ["Limited personalization", "Manual optimization"],
                "priority_actions": ["AI-powered personalization", "Automated A/B testing"]
            }
        },
        overall_score=150,
        recommendations=[
            "Implement comprehensive AI automation strategy",
            "Focus on high-impact areas: scaling and competitor analysis",
            "Prioritize AI integration in customer-facing processes",
            "Develop team AI literacy and capabilities"
        ],
        created_at=datetime.now()
    )

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

@app.post("/auth/login")
async def login_user(user_auth: UserAuth):
    user_id = str(uuid.uuid4())
    users_db[user_id] = {
        "email": user_auth.email,
        "name": user_auth.name,
        "mobile": user_auth.mobile,
        "created_at": datetime.now()
    }
    return {"user_id": user_id, "message": "User authenticated successfully"}

class CreateTestResultRequest(BaseModel):
    user_id: str

@app.post("/test-results", response_model=TestResultResponse)
async def create_test_result(request: CreateTestResultRequest):
    if request.user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    result = create_sample_result(request.user_id)
    result_id = str(uuid.uuid4())
    test_results_db[result_id] = result
    
    user = users_db[request.user_id]
    return TestResultResponse(
        id=result_id,
        user_email=user["email"],
        user_name=user["name"],
        pain_points=result.pain_points,
        categories=result.categories,
        overall_score=result.overall_score,
        recommendations=result.recommendations,
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
        pain_points=result.pain_points,
        categories=result.categories,
        overall_score=result.overall_score,
        recommendations=result.recommendations,
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
