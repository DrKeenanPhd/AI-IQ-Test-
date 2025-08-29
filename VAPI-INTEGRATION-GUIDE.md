# VAPI AI Agent Integration Guide

## Complete Workflow: VAPI → GHL → Dynamic Site

This guide explains the complete integration workflow for connecting your VAPI AI agent to GHL custom fields and dynamic site population.

## Architecture Overview

```
[User] → [VAPI AI Call] → [Structured JSON] → [GHL Webhook] → [Custom Fields]
                                                     ↓
[Your Site] ← [Site Webhook] ← [GHL Workflow] ← [Contact Updated]
```

## Phase 1: VAPI Agent Configuration

### 1.1 Agent Setup
Configure your VAPI agent to output structured JSON using the schema in `/config/vapi_integration.json`:

```javascript
// VAPI Agent Configuration
{
  "name": "AI IQ Test Agent",
  "model": "gpt-4",
  "voice": "your-preferred-voice",
  "functions": [],
  "endCallMessage": "Thank you for completing the AI IQ assessment. Your comprehensive report will be available shortly.",
  "endCallFunctionEnabled": true,
  "serverUrl": "https://hooks.gohighlevel.com/webhook/your-webhook-id",
  "serverUrlSecret": "your-webhook-secret"
}
```

### 1.2 JSON Output Schema
Your VAPI agent should generate JSON matching this structure:

```json
{
  "contact_info": {
    "email": "user@example.com",
    "name": "John Doe", 
    "phone": "+1234567890",
    "company": "Example Corp"
  },
  "pain_points": {
    "cant_scale_without_burnout": {
      "score": 75,
      "severity": "high",
      "description": "Company struggles with manual processes",
      "evidence": ["Working 60+ hour weeks", "Manual data entry"],
      "impact_areas": ["productivity", "employee_satisfaction"]
    },
    // ... other pain points
  },
  "categories": {
    "website_form_function": {
      "score": 65,
      "percentage": 65,
      "strengths": ["Mobile responsive", "Fast loading"],
      "weaknesses": ["Poor SEO", "No AI integration"],
      "priority_actions": ["Implement chatbot", "Optimize for search"]
    },
    // ... other categories
  },
  "overall_assessment": {
    "overall_score": 68,
    "ai_readiness_level": "intermediate",
    "priority_recommendations": ["Implement AI chatbot", "Automate lead scoring"],
    "quick_wins": ["Add live chat", "Set up email automation"],
    "next_steps": ["Schedule AI strategy session", "Audit current tools"]
  }
}
```

## Phase 2: GHL Integration Setup

### 2.1 Create Custom Fields in GHL
Add these custom fields to your GHL location:

**Core Fields:**
- `ai_iq_test_results` (Long Text) - Full JSON payload
- `ai_iq_overall_score` (Number) - Overall score 0-100
- `ai_iq_readiness_level` (Text) - beginner|intermediate|advanced|expert
- `ai_iq_test_date` (Date) - When test was completed

**Pain Point Scores:**
- `ai_iq_cant_scale_score` (Number)
- `ai_iq_invisible_score` (Number) 
- `ai_iq_outgunned_score` (Number)
- `ai_iq_tech_gap_score` (Number)

**Category Scores:**
- `ai_iq_website_score` (Number)
- `ai_iq_social_score` (Number)
- `ai_iq_digital_score` (Number)
- `ai_iq_communication_score` (Number)
- `ai_iq_marketing_score` (Number)

**Action Items:**
- `ai_iq_priority_actions` (Long Text) - JSON array
- `ai_iq_quick_wins` (Long Text) - JSON array
- `ai_iq_next_steps` (Long Text) - JSON array

### 2.2 Configure GHL Webhook
1. Go to GHL Settings → Integrations → Webhooks
2. Create new webhook with URL: `https://hooks.gohighlevel.com/webhook/your-webhook-id`
3. Set trigger: "Contact Custom Field Updated"
4. Select fields: `ai_iq_test_results`

### 2.3 Create GHL Workflow
**Trigger:** Contact custom field `ai_iq_test_results` is updated
**Actions:**
1. **Wait** 2 seconds (allow field updates to complete)
2. **HTTP POST** to your site webhook:
   - URL: `https://your-site.com/api/webhooks/vapi-result`
   - Method: POST
   - Headers: `Content-Type: application/json`
   - Body: 
   ```json
   {
     "contact_id": "{{contact.id}}",
     "email": "{{contact.email}}",
     "name": "{{contact.name}}",
     "phone": "{{contact.phone}}",
     "test_results": "{{contact.custom_field.ai_iq_test_results}}",
     "overall_score": "{{contact.custom_field.ai_iq_overall_score}}"
   }
   ```

## Phase 3: Site Integration (Already Built!)

### 3.1 Webhook Endpoint
Your site already has the endpoint `/api/webhooks/vapi-result` that:
- Receives GHL webhook notifications
- Processes VAPI test results
- Generates dynamic reports
- Stores results in database

### 3.2 Dynamic Report Generation
The existing system automatically:
- Parses JSON from GHL custom fields
- Maps to internal data structures
- Generates responsive report layouts
- Adapts grid layouts based on content size

## Phase 4: Testing & Validation

### 4.1 Test VAPI Agent
1. Configure VAPI agent with webhook URL
2. Make test call and verify JSON output
3. Check GHL custom fields are populated
4. Verify site webhook receives notification

### 4.2 Validate Data Flow
```bash
# Test VAPI webhook (simulate agent output)
curl -X POST https://hooks.gohighlevel.com/webhook/your-webhook-id \
  -H "Content-Type: application/json" \
  -d @test_vapi_output.json

# Check GHL contact fields updated
# Verify site webhook triggered
# Confirm report generated on site
```

## Environment Variables Required

### Backend (.env)
```bash
# VAPI Integration
VAPI_API_KEY=your_vapi_api_key
VAPI_ASSISTANT_ID=your_assistant_id
VAPI_BASE_URL=https://api.vapi.ai

# GHL Integration (existing)
GHL_API_KEY=your_ghl_api_key
GHL_LOCATION_ID=your_location_id

# Site Webhook
SITE_WEBHOOK_URL=https://your-site.com/api/webhooks/vapi-result
```

## Advanced Features

### Real-time Updates
- WebSocket connections for live report updates
- Progress indicators during AI analysis
- Instant notifications when test completes

### Data Validation
- JSON schema validation for VAPI output
- Error handling for malformed data
- Retry logic for failed webhooks

### Analytics & Insights
- Track test completion rates
- Monitor AI confidence scores
- Analyze common pain points across users

## Troubleshooting

### Common Issues
1. **VAPI webhook not triggering**: Check webhook URL and authentication
2. **GHL fields not updating**: Verify field names match exactly
3. **Site not receiving notifications**: Check GHL workflow configuration
4. **JSON parsing errors**: Validate VAPI output against schema

### Debug Steps
1. Check VAPI agent logs for webhook calls
2. Verify GHL webhook delivery logs
3. Monitor site webhook endpoint logs
4. Validate JSON structure matches schema

## Implementation Timeline

**Phase 1 (VAPI Setup)**: 30-45 minutes
- Configure agent with JSON schema
- Set webhook URL
- Test output format

**Phase 2 (GHL Configuration)**: 45-60 minutes  
- Create custom fields
- Set up webhook
- Configure workflow

**Phase 3 (Testing)**: 30 minutes
- End-to-end testing
- Validation and debugging

**Total**: 2-2.5 hours for complete integration

The beauty of this system is that your site is already built to handle the dynamic report generation - we just need to connect the VAPI → GHL data pipeline!
