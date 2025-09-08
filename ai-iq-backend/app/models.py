from pydantic import BaseModel, EmailStr
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from enum import Enum

class SeverityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class SectionType(str, Enum):
    PAIN_POINT = "pain_point"
    CATEGORY = "category"
    CUSTOM = "custom"
    RECOMMENDATION = "recommendation"

class UserAuth(BaseModel):
    email: EmailStr
    name: str
    mobile: str

class GHLContact(BaseModel):
    id: str
    email: str
    name: str
    phone: str
    custom_fields: Dict[str, Any] = {}
    tags: List[str] = []

class TestParameter(BaseModel):
    name: str
    value: Union[str, int, float, bool]
    weight: float = 1.0
    category: Optional[str] = None

class DynamicSection(BaseModel):
    title: str
    content: Dict[str, Any]
    display_order: int
    section_type: SectionType
    is_expandable: bool = True
    min_height: Optional[str] = None
    max_height: Optional[str] = None

class PainPoint(BaseModel):
    score: int
    description: str
    severity: SeverityLevel
    recommendations: List[str]
    impact_areas: List[str] = []
    custom_data: Dict[str, Any] = {}

class Category(BaseModel):
    score: int
    max_score: int
    percentage: float
    strengths: List[str]
    weaknesses: List[str]
    priority_actions: List[str]
    custom_metrics: Dict[str, Any] = {}

class DynamicTestResult(BaseModel):
    user_id: str
    schema_version: Optional[str] = None
    score_max: int = 200
    overall_score: int
    overall_score_norm: Optional[float] = None  # 0-100 normalized for visuals
    pain_points: Dict[str, PainPoint]
    categories: Dict[str, Category]
    recommendations: List[str]
    custom_sections: Optional[Dict[str, DynamicSection]] = None
    test_parameters: Optional[Dict[str, TestParameter]] = None
    report_metadata: Optional[Dict[str, Any]] = None
    created_at: datetime = datetime.now()

class ROIAnalysis(BaseModel):
    estimated_monthly_savings: float
    implementation_cost: float
    roi_percentage: float
    payback_period_months: int
    productivity_gains: List[str]
    cost_reduction_areas: List[str]
    revenue_opportunities: List[str]
    risk_mitigation_value: float

class DetailedReport(BaseModel):
    executive_summary: str
    current_state_analysis: Dict[str, Any]
    recommended_solutions: List[Dict[str, Any]]
    implementation_roadmap: List[Dict[str, Any]]
    success_metrics: List[str]
    next_steps: List[str]
    appendix_data: Optional[Dict[str, Any]] = None

class TestResultResponse(BaseModel):
    id: str
    user_email: str
    user_name: str
    contact_id: Optional[str] = None
    session_id: Optional[str] = None
    pain_points: Dict[str, Dict[str, Any]]
    categories: Dict[str, Dict[str, Any]]
    overall_score: int
    recommendations: List[str]
    custom_sections: Optional[Dict[str, Dict[str, Any]]] = None
    report_metadata: Optional[Dict[str, Any]] = None
    created_at: datetime
    
    session_metadata: Optional[Dict[str, Any]] = None
    voice_summary: Optional[Dict[str, Any]] = None
    api_data_sources: Optional[Dict[str, Any]] = None
    subscription_recommendations: Optional[Dict[str, Any]] = None
    roi_analysis: Optional[ROIAnalysis] = None
    detailed_report: Optional[DetailedReport] = None

class CreateTestResultRequest(BaseModel):
    user_id: str
    test_parameters: Optional[Dict[str, Any]] = None
    ghl_contact_data: Optional[Dict[str, Any]] = None

class GHLWebhookData(BaseModel):
    contact_id: str
    email: str
    name: str
    phone: str
    form_data: Dict[str, Any]
    custom_fields: Dict[str, Any] = {}

class ConfigurationSettings(BaseModel):
    pain_point_weights: Dict[str, float] = {}
    category_weights: Dict[str, float] = {}
    scoring_thresholds: Dict[str, int] = {}
    dynamic_sections_enabled: bool = True
    max_custom_sections: int = 10

class SubscriptionStatus(str, Enum):
    TRIAL = "trial"
    ACTIVE = "active"
    CANCELLED = "cancelled"
    EXPIRED = "expired"
    PAST_DUE = "past_due"

class UserSubscription(BaseModel):
    user_id: str
    subscription_status: SubscriptionStatus = SubscriptionStatus.TRIAL
    trial_start_date: Optional[datetime] = None
    trial_end_date: Optional[datetime] = None
    stripe_customer_id: Optional[str] = None
    stripe_subscription_id: Optional[str] = None
    current_period_start: Optional[datetime] = None
    current_period_end: Optional[datetime] = None
    created_at: datetime = datetime.now()

class CreateSubscriptionRequest(BaseModel):
    user_id: str
    payment_method_id: str
    
class SubscriptionResponse(BaseModel):
    subscription_id: str
    client_secret: Optional[str] = None
    status: str
    trial_end: Optional[datetime] = None
    current_period_end: Optional[datetime] = None

class StripeWebhookEvent(BaseModel):
    id: str
class TestRunType(str, Enum):
    FULL = "full"
    MINI = "mini"

class TestRunStatus(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETE = "complete"
    FAILED = "failed"

class TestRun(BaseModel):
    id: str
    user_id: str
    type: TestRunType
    topic: Optional[str] = None  # for mini-tests, e.g., website/social/search
    status: TestRunStatus = TestRunStatus.QUEUED
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    score: Optional[float] = None
    payload: Optional[Dict[str, Any]] = None
    source: Optional[str] = None  # agent|ui
    created_by: Optional[str] = None

class IQScore(BaseModel):
    id: str
    user_id: str
    score: float
    period_month: str  # e.g., "2025-09"
    computed_at: datetime = datetime.now()
    delta_vs_prev: Optional[float] = None
    type: str
    data: Dict[str, Any]
