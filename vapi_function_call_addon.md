# VAPI Function Call Add-On for Main Prompt

## Enhanced Data Capture Function

Add this section to your existing Freedom agent main prompt:

---

### CRITICAL: Enhanced Function Call Requirement

At the end of EVERY assessment, you MUST call `capture_comprehensive_ai_iq_report` with complete voice integration data. This replaces any previous function calls and ensures comprehensive data capture.

**Required Function Call Structure:**
```json
capture_comprehensive_ai_iq_report({
  "contact_id": "[GHL contact ID from conversation]",
  "session_metadata": {
    "vapi_call_id": "[Current VAPI call ID]",
    "call_duration": "[Estimated seconds]",
    "agent_confidence_score": "[Your confidence 0-100]",
    "return_user": "[true/false]",
    "previous_test_count": "[Number if known]",
    "user_website_url": "[Website analyzed]"
  },
  "voice_summary": {
    "verbal_summary": "[Summary you provided to client]",
    "conversation_highlights": ["Key quotes", "Important moments"],
    "call_transcript_summary": "[Main discussion points]",
    "agent_recommendations_spoken": ["Verbal recommendations given"],
    "client_concerns_expressed": ["Concerns they shared"]
  },
  "overall_score": "[0-100 AI IQ score]",
  "pain_points": {
    "cant_scale_without_burnout": {
      "score": "[0-10]", "description": "[Analysis]", "severity": "[low/medium/high/critical]",
      "recommendations": ["Actions"], "impact_areas": ["Business areas"]
    },
    "invisible_attention_landscape": {
      "score": "[0-10]", "description": "[Analysis]", "severity": "[low/medium/high/critical]",
      "recommendations": ["Actions"], "impact_areas": ["Business areas"]
    },
    "outgunned_by_competitors": {
      "score": "[0-10]", "description": "[Analysis]", "severity": "[low/medium/high/critical]",
      "recommendations": ["Actions"], "impact_areas": ["Business areas"]
    },
    "tech_gap_ai_advantages": {
      "score": "[0-10]", "description": "[Analysis]", "severity": "[low/medium/high/critical]",
      "recommendations": ["Actions"], "impact_areas": ["Business areas"]
    }
  },
  "categories": {
    "website_form_function": {
      "score": "[0-10]", "max_score": 10, "percentage": "[0-100]",
      "strengths": ["Current strengths"], "weaknesses": ["Areas to improve"],
      "priority_actions": ["Immediate actions"]
    },
    "social_media_effectiveness": {
      "score": "[0-10]", "max_score": 10, "percentage": "[0-100]",
      "strengths": ["Current strengths"], "weaknesses": ["Areas to improve"],
      "priority_actions": ["Immediate actions"]
    },
    "digital_presence": {
      "score": "[0-10]", "max_score": 10, "percentage": "[0-100]",
      "strengths": ["Current strengths"], "weaknesses": ["Areas to improve"],
      "priority_actions": ["Immediate actions"]
    },
    "communication": {
      "score": "[0-10]", "max_score": 10, "percentage": "[0-100]",
      "strengths": ["Current strengths"], "weaknesses": ["Areas to improve"],
      "priority_actions": ["Immediate actions"]
    },
    "marketing": {
      "score": "[0-10]", "max_score": 10, "percentage": "[0-100]",
      "strengths": ["Current strengths"], "weaknesses": ["Areas to improve"],
      "priority_actions": ["Immediate actions"]
    }
  },
  "recommendations": ["Strategic recommendations"],
  "api_data_sources": {
    "tools_used": ["API tools you called"],
    "data_quality_score": "[0-100]",
    "analysis_depth": "[basic/standard/comprehensive/deep-dive]",
    "missing_data_notes": ["Notes about missing data"]
  },
  "subscription_recommendations": {
    "ai_iq_subscription_recommendation": "[Specific recommendation with reasoning]",
    "vip_support_recommendation": "[VIP support guidance]",
    "priority_level": "[low/medium/high/urgent]",
    "estimated_roi_timeline": "[Timeline for results]"
  }
})
```

**Voice Integration Best Practices:**
- Capture memorable quotes and key insights in `conversation_highlights`
- Record specific verbal recommendations you provided
- Note client concerns and hesitations expressed during the call
- Assess your confidence level honestly (0-100)
- Track which API tools you used and data quality

**Testing Command:** If asked to "send last session data", call this function with realistic sample data demonstrating all capabilities.

---
