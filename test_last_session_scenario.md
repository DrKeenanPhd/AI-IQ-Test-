# Test Command: "Send Last Session Data"

## Quick Test for Agent
Ask your Freedom agent: **"Can you send the data from your last session to test the new reporting system?"**

## Expected Agent Response
The agent should call `capture_comprehensive_ai_iq_report` with realistic sample data demonstrating:
- Complete session metadata (call duration, confidence score, website URL)
- Voice summary (verbal summary provided, conversation highlights, recommendations spoken)
- Full pain points analysis (all 4 categories with scores and severity)
- Complete context assessment (all 5 areas with percentages and actions)
- API data sources tracking
- Subscription recommendations with priority levels

## Sample Test Data Response
```json
{
  "contact_id": "test_contact_12345",
  "session_metadata": {
    "vapi_call_id": "test_call_67890",
    "call_duration": 720,
    "agent_confidence_score": 85,
    "return_user": false,
    "previous_test_count": 0,
    "user_website_url": "https://example-business.com"
  },
  "voice_summary": {
    "verbal_summary": "Based on our 12-minute assessment, your business shows strong potential but has key gaps in AI implementation that are limiting growth. You're currently scoring 42 out of 100 on our AI IQ scale, with the biggest opportunities in automation and competitive positioning.",
    "conversation_highlights": [
      "Client mentioned struggling with manual lead qualification taking 3+ hours daily",
      "Expressed frustration: 'I feel like I'm working harder, not smarter'",
      "Interested in AI solutions but concerned about implementation complexity",
      "Revealed competitors are using chatbots while they still rely on phone calls",
      "Excited about potential ROI: 'If I could save 15 hours a week, that would be game-changing'"
    ],
    "call_transcript_summary": "Discussed current marketing challenges, website performance issues, and competitive positioning. Client operates a consulting business with 5 employees and $500K annual revenue. Main pain points include manual lead qualification, slow response times, and falling behind AI-enabled competitors. Website analysis revealed good design but missing AI tools and optimization.",
    "agent_recommendations_spoken": [
      "Start with AI chatbot for initial lead qualification - could save 15+ hours per week",
      "Implement automated email sequences for nurturing prospects",
      "Add AI-powered content generation for blog posts and social media",
      "Consider AI lead scoring to prioritize high-value prospects",
      "Optimize website for AI search engines with structured data"
    ],
    "client_concerns_expressed": [
      "Worried about AI implementation costs and ROI timeline",
      "Concerned about learning curve for new tools and team training",
      "Unsure about which AI tools to prioritize first",
      "Hesitant about losing personal touch with automated systems",
      "Questioned whether AI would work for their specific industry"
    ]
  },
  "overall_score": 42,
  "pain_points": {
    "cant_scale_without_burnout": {
      "score": 8,
      "description": "Heavy reliance on manual processes for lead qualification and content creation. Owner spending 60% of time on tasks that could be automated, including 3+ hours daily on lead qualification, manual email follow-ups, and content creation. No automation systems in place.",
      "severity": "high",
      "recommendations": [
        "Implement AI lead scoring system",
        "Automate email nurture sequences", 
        "Deploy chatbot for initial qualification",
        "Use AI content generation tools"
      ],
      "impact_areas": ["Time management", "Team productivity", "Growth capacity", "Work-life balance"]
    },
    "invisible_attention_landscape": {
      "score": 6,
      "description": "Limited visibility in AI-powered search results. Website lacks AI-optimized content, schema markup, and structured data. Not appearing in AI search results when prospects ask questions about their services.",
      "severity": "medium",
      "recommendations": [
        "Optimize content for AI search engines",
        "Add structured data markup",
        "Create FAQ content for AI assistants",
        "Implement voice search optimization"
      ],
      "impact_areas": ["Online visibility", "Lead generation", "Brand awareness", "Organic traffic"]
    },
    "outgunned_by_competitors": {
      "score": 7,
      "description": "Competitors using AI chatbots, automated nurture sequences, and instant response systems. Falling behind in response time (24+ hours vs competitors' instant responses) and personalization capabilities.",
      "severity": "high",
      "recommendations": [
        "Deploy AI customer service chatbot",
        "Implement automated lead nurturing",
        "Add instant response capabilities",
        "Use AI for personalized messaging"
      ],
      "impact_areas": ["Customer experience", "Conversion rates", "Market share", "Competitive advantage"]
    },
    "tech_gap_ai_advantages": {
      "score": 9,
      "description": "No AI tools currently implemented. Missing opportunities for automation, personalization, predictive analytics, and data-driven insights. Completely manual operations in an increasingly AI-driven market.",
      "severity": "critical",
      "recommendations": [
        "Start with AI content creation tools",
        "Implement predictive analytics for forecasting",
        "Deploy AI-powered CRM automation",
        "Use AI for customer behavior analysis"
      ],
      "impact_areas": ["Operational efficiency", "Decision making", "Competitive advantage", "Revenue growth"]
    }
  },
  "categories": {
    "website_form_function": {
      "score": 6,
      "max_score": 10,
      "percentage": 60,
      "strengths": ["Clean, professional design", "Mobile responsive layout", "Fast loading speed", "Clear value proposition"],
      "weaknesses": ["No chatbot or live chat", "Basic contact forms only", "Limited personalization", "No AI-powered features"],
      "priority_actions": ["Add AI chatbot", "Implement dynamic content", "Optimize conversion paths", "Add lead magnets"]
    },
    "social_media_effectiveness": {
      "score": 4,
      "max_score": 10,
      "percentage": 40,
      "strengths": ["Consistent posting schedule", "Professional imagery", "Industry-relevant content"],
      "weaknesses": ["Manual posting process", "Low engagement rates", "No AI optimization", "Limited audience growth"],
      "priority_actions": ["Automate posting schedule", "Use AI for content creation", "Implement engagement analytics", "Add social listening tools"]
    },
    "digital_presence": {
      "score": 5,
      "max_score": 10,
      "percentage": 50,
      "strengths": ["Good domain authority", "Basic SEO foundation", "Professional online listings"],
      "weaknesses": ["Limited AI search visibility", "No schema markup", "Outdated content strategy", "Poor local SEO"],
      "priority_actions": ["Optimize for AI search", "Add structured data", "Create AI-friendly content", "Improve local SEO"]
    },
    "communication": {
      "score": 3,
      "max_score": 10,
      "percentage": 30,
      "strengths": ["Personal touch in interactions", "Industry expertise", "Professional tone"],
      "weaknesses": ["Slow response times (24+ hours)", "Manual email processes", "No automation", "Limited availability"],
      "priority_actions": ["Implement AI chatbot", "Automate email sequences", "Add instant response systems", "Create FAQ automation"]
    },
    "marketing": {
      "score": 4,
      "max_score": 10,
      "percentage": 40,
      "strengths": ["Clear value proposition", "Targeted messaging", "Industry focus"],
      "weaknesses": ["Manual lead qualification", "No predictive analytics", "Limited personalization", "Poor lead nurturing"],
      "priority_actions": ["Implement AI lead scoring", "Add predictive analytics", "Automate nurture campaigns", "Personalize messaging"]
    }
  },
  "recommendations": [
    "Start with AI chatbot implementation for immediate impact on lead qualification and response times",
    "Automate content creation workflow to free up 15+ hours per week for strategic activities",
    "Implement predictive analytics to improve decision making and revenue forecasting",
    "Deploy AI-powered email marketing for better personalization and higher conversion rates",
    "Optimize website and content for AI search engines to improve visibility"
  ],
  "api_data_sources": {
    "tools_used": ["BuiltWith", "SerpAPI", "Moz SEO"],
    "data_quality_score": 75,
    "analysis_depth": "comprehensive",
    "missing_data_notes": [
      "Social media analytics not available due to privacy settings",
      "Competitor pricing data limited",
      "Email marketing metrics not accessible"
    ]
  },
  "subscription_recommendations": {
    "ai_iq_subscription_recommendation": "Highly recommended - Your business shows strong potential for 3-5x ROI within 6 months through AI implementation. The Business Analysis tool will provide ongoing optimization, performance tracking, and strategic guidance to maximize your AI investments.",
    "vip_support_recommendation": "Recommended for first 90 days - Given the complexity of implementing multiple AI tools and your current manual processes, VIP support will ensure smooth deployment, proper training, and maximize early wins while minimizing disruption.",
    "priority_level": "high",
    "estimated_roi_timeline": "Initial improvements within 30 days (chatbot and automation), significant ROI within 3-6 months (full AI implementation)"
  }
}
```

## Testing Validation Checklist

### ✅ Session Metadata Validation
- [ ] `vapi_call_id` is present and realistic
- [ ] `call_duration` is reasonable (300-1800 seconds typical)
- [ ] `agent_confidence_score` is between 0-100
- [ ] `return_user` is boolean
- [ ] `user_website_url` is valid URL format

### ✅ Voice Summary Validation
- [ ] `verbal_summary` contains realistic summary language
- [ ] `conversation_highlights` has 3-7 meaningful quotes/insights
- [ ] `call_transcript_summary` covers main discussion points
- [ ] `agent_recommendations_spoken` lists specific verbal advice
- [ ] `client_concerns_expressed` captures realistic business concerns

### ✅ Core Analysis Validation
- [ ] `overall_score` is 0-100 and matches pain point analysis
- [ ] All 4 pain points have scores 0-10, descriptions, and severity levels
- [ ] All 5 categories have scores, percentages, strengths, weaknesses, and actions
- [ ] Recommendations are specific and actionable

### ✅ Enhanced Features Validation
- [ ] `api_data_sources` lists realistic tools and data quality assessment
- [ ] `subscription_recommendations` includes both AI IQ and VIP support guidance
- [ ] Priority level is one of: low/medium/high/urgent
- [ ] ROI timeline is realistic and specific

## Success Indicators
1. **Function Call Executes**: Agent successfully calls the function without errors
2. **Data Completeness**: All required fields are populated with realistic data
3. **Voice Integration**: Voice summary fields contain meaningful conversation data
4. **Analysis Quality**: Scores and recommendations align with business scenario
5. **System Integration**: Data flows to GHL custom fields and Supabase correctly
6. **Report Generation**: Personalized report page is created and accessible

## Troubleshooting Common Issues
- **Schema Validation Errors**: Check that all required fields are present
- **Function Not Found**: Verify tool is properly imported and assigned to agent
- **Empty Voice Data**: Ensure agent is instructed to capture conversation details
- **Unrealistic Scores**: Validate that pain point scores align with overall assessment
- **Missing API Data**: Check if agent has access to external tools for analysis
