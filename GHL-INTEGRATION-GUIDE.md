# GoHighLevel Integration Guide

## Overview
This guide explains how to integrate your AI IQ Test Results platform with GoHighLevel (GHL) for seamless contact management, authentication, and dynamic report generation.

## 1. GHL Configuration Files

### Backend Environment Variables (.env)
```bash
# GoHighLevel API Configuration
GHL_API_KEY=your_ghl_api_key_here
GHL_LOCATION_ID=your_ghl_location_id_here
GHL_BASE_URL=https://services.leadconnectorhq.com

# Optional: Webhook configuration
GHL_WEBHOOK_SECRET=your_webhook_secret_here
```

### GHL API Client Configuration
Create `ai-iq-backend/app/ghl_client.py`:
```python
import httpx
import os
from typing import Dict, Any, Optional

class GHLClient:
    def __init__(self):
        self.api_key = os.getenv("GHL_API_KEY")
        self.location_id = os.getenv("GHL_LOCATION_ID")
        self.base_url = os.getenv("GHL_BASE_URL", "https://services.leadconnectorhq.com")
        
    async def create_or_update_contact(self, email: str, name: str, mobile: str, custom_fields: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create or update a contact in GHL"""
        
    async def get_contact_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Retrieve contact from GHL by email"""
        
    async def update_contact_custom_fields(self, contact_id: str, custom_fields: Dict[str, Any]) -> bool:
        """Update custom fields for a contact"""
```

## 2. Authentication Integration with GHL

### Modified Authentication Flow
```python
# In ai-iq-backend/app/main.py
from .ghl_client import GHLClient

@app.post("/auth/login")
async def login_user(user_auth: UserAuth):
    ghl_client = GHLClient()
    
    # Check if contact exists in GHL
    existing_contact = await ghl_client.get_contact_by_email(user_auth.email)
    
    if existing_contact:
        # Update existing contact
        contact_id = existing_contact["id"]
        await ghl_client.create_or_update_contact(
            email=user_auth.email,
            name=user_auth.name,
            mobile=user_auth.mobile
        )
    else:
        # Create new contact in GHL
        contact_data = await ghl_client.create_or_update_contact(
            email=user_auth.email,
            name=user_auth.name,
            mobile=user_auth.mobile,
            custom_fields={
                "ai_iq_test_taken": "true",
                "signup_source": "AI IQ Test Platform"
            }
        )
        contact_id = contact_data["contact"]["id"]
    
    # Store GHL contact ID with user
    user_id = str(uuid.uuid4())
    users_db[user_id] = {
        "email": user_auth.email,
        "name": user_auth.name,
        "mobile": user_auth.mobile,
        "ghl_contact_id": contact_id,
        "created_at": datetime.now()
    }
    
    return {"user_id": user_id, "ghl_contact_id": contact_id, "message": "User authenticated successfully"}
```

## 3. Dynamic Report Population from GHL

### GHL Custom Fields for AI IQ Test
Set up these custom fields in your GHL location:

**Pain Points Fields:**
- `ai_iq_cant_scale_score` (Number)
- `ai_iq_invisible_attention_score` (Number)
- `ai_iq_outgunned_competitors_score` (Number)
- `ai_iq_tech_gap_score` (Number)

**Category Fields:**
- `ai_iq_website_score` (Number)
- `ai_iq_social_media_score` (Number)
- `ai_iq_digital_presence_score` (Number)
- `ai_iq_communication_score` (Number)
- `ai_iq_marketing_score` (Number)

**Overall Fields:**
- `ai_iq_overall_score` (Number)
- `ai_iq_test_date` (Date)
- `ai_iq_report_json` (Text - stores full JSON)

### Dynamic Report Generation
```python
@app.post("/test-results", response_model=TestResultResponse)
async def create_test_result(request: CreateTestResultRequest):
    if request.user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = users_db[request.user_id]
    ghl_client = GHLClient()
    
    # Check if contact has existing test data in GHL
    contact = await ghl_client.get_contact_by_email(user["email"])
    
    if contact and contact.get("customFields"):
        # Use existing GHL data if available
        result = create_result_from_ghl_data(contact["customFields"], request.user_id)
    else:
        # Generate new sample result
        result = create_sample_result(request.user_id)
        
        # Save results back to GHL
        await ghl_client.update_contact_custom_fields(
            user["ghl_contact_id"],
            {
                "ai_iq_overall_score": result.overall_score,
                "ai_iq_test_date": result.created_at.isoformat(),
                "ai_iq_report_json": json.dumps({
                    "pain_points": result.pain_points,
                    "categories": result.categories,
                    "recommendations": result.recommendations
                })
            }
        )
    
    result_id = str(uuid.uuid4())
    test_results_db[result_id] = result
    
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
```

## 4. Adaptive Report Structure

### Dynamic Report Schema
```python
class DynamicTestResult(BaseModel):
    user_id: str
    pain_points: Dict[str, Dict[str, Any]]  # Flexible structure
    categories: Dict[str, Dict[str, Any]]   # Flexible structure
    overall_score: int
    recommendations: List[str]
    custom_sections: Optional[Dict[str, Any]] = None  # For expandable content
    report_metadata: Optional[Dict[str, Any]] = None  # Size, version, etc.
    created_at: datetime

class ReportSection(BaseModel):
    title: str
    content: Dict[str, Any]
    display_order: int
    section_type: str  # "pain_point", "category", "custom", "recommendation"
    is_expandable: bool = True
```

### Frontend Adaptive Rendering
```typescript
// In App.tsx - Add dynamic section rendering
const renderDynamicSection = (sectionKey: string, sectionData: any) => {
  if (!sectionData) return null;
  
  return (
    <Card key={sectionKey} className="bg-gray-800/50 border-gray-700 backdrop-blur-sm">
      <CardHeader>
        <CardTitle className="text-white">{sectionData.title || formatSectionName(sectionKey)}</CardTitle>
      </CardHeader>
      <CardContent>
        {sectionData.subsections ? (
          // Render nested subsections
          Object.entries(sectionData.subsections).map(([subKey, subData]: [string, any]) => (
            <div key={subKey} className="mb-4">
              <h4 className="text-lg font-semibold text-white mb-2">{subData.title}</h4>
              {renderSectionContent(subData)}
            </div>
          ))
        ) : (
          renderSectionContent(sectionData)
        )}
      </CardContent>
    </Card>
  );
};

// Add to main render after existing sections
{testResult.custom_sections && Object.entries(testResult.custom_sections).map(([key, section]: [string, any]) => 
  renderDynamicSection(key, section)
)}
```

## 5. GHL Dynamic Forms Integration

### Form Builder Integration
```javascript
// GHL Form webhook endpoint
@app.post("/webhooks/ghl-form")
async def handle_ghl_form_submission(form_data: Dict[str, Any]):
    """Handle form submissions from GHL and trigger AI IQ test"""
    
    email = form_data.get("email")
    name = form_data.get("name") 
    mobile = form_data.get("phone")
    
    # Extract any pre-filled test parameters
    test_params = {
        "industry": form_data.get("industry"),
        "company_size": form_data.get("company_size"),
        "current_ai_usage": form_data.get("ai_usage_level"),
        "primary_challenges": form_data.get("challenges", [])
    }
    
    # Create user and generate customized test
    user_auth = UserAuth(email=email, name=name, mobile=mobile)
    auth_result = await login_user(user_auth)
    
    # Generate test results based on form parameters
    customized_result = await create_customized_test_result(
        auth_result["user_id"], 
        test_params
    )
    
    return {"status": "success", "test_result_id": customized_result.id}
```

### GHL Workflow Triggers
Set up these workflows in GHL:
1. **New Contact Created** → Trigger AI IQ Test invitation
2. **Form Submitted** → Auto-generate test results
3. **Test Completed** → Add to nurture sequence
4. **High Score Achieved** → Trigger sales team notification

## 6. Subscription Integration

### Monthly Billing Setup
```python
# Add subscription tracking
class UserSubscription(BaseModel):
    user_id: str
    ghl_contact_id: str
    subscription_status: str  # "active", "cancelled", "trial"
    billing_cycle: str
    next_billing_date: datetime
    ai_assistant_access: bool = False

@app.post("/subscriptions/activate")
async def activate_subscription(user_id: str, subscription_type: str):
    """Activate AI assistant subscription"""
    user = users_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update GHL contact with subscription info
    ghl_client = GHLClient()
    await ghl_client.update_contact_custom_fields(
        user["ghl_contact_id"],
        {
            "subscription_status": "active",
            "ai_assistant_access": "true",
            "subscription_start_date": datetime.now().isoformat()
        }
    )
    
    return {"status": "activated", "access_granted": True}
```

## 7. Implementation Steps

1. **Set up GHL API credentials** in your backend environment
2. **Create custom fields** in your GHL location for AI IQ data
3. **Implement GHL client** in your backend
4. **Update authentication flow** to sync with GHL contacts
5. **Modify report generation** to use GHL data when available
6. **Set up webhooks** for form submissions and subscription changes
7. **Create GHL workflows** for automated follow-up sequences
8. **Test integration** with sample contacts and forms

## 8. Testing Checklist

- [ ] Contact creation/update in GHL works
- [ ] Custom fields are properly populated
- [ ] Form submissions trigger test generation
- [ ] Report data syncs back to GHL
- [ ] Subscription status updates correctly
- [ ] Webhooks handle all scenarios
- [ ] Error handling for API failures

This integration will make your AI IQ Test platform a seamless part of your GHL ecosystem!

## Implementation Status

✅ **Backend Models**: Enhanced Pydantic models with dynamic sections and GHL integration
✅ **GHL Client**: Full API client with contact management and parameter extraction  
✅ **Test Engine**: Dynamic scoring system with configurable parameters and custom sections
✅ **API Endpoints**: Updated authentication, test generation, and webhook handling
✅ **Frontend Rendering**: Adaptive grid layouts and custom section support
✅ **Configuration System**: Environment variables and JSON-based parameter configuration

## Quick Start

1. **Configure GHL credentials** in `ai-iq-backend/.env`:
```bash
GHL_API_KEY=your_api_key_here
GHL_LOCATION_ID=your_location_id_here
```

2. **Customize test parameters** in `config/test_parameters.json`

3. **Deploy and test** - the system gracefully handles missing GHL credentials for development

The platform now supports:
- Dynamic report sizing based on content
- GHL contact synchronization
- Configurable test parameters and weighting
- Custom sections for industry-specific insights
- Webhook integration for form submissions
