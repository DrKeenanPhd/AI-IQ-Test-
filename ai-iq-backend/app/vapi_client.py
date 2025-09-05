import httpx
import os
import time
from typing import Dict, Any, Optional
import json
import logging
from datetime import datetime
from .models import DynamicTestResult, PainPoint, Category, SeverityLevel, TestParameter
from .ghl_client import GHLClient
from .smart_links import SmartLink

logger = logging.getLogger(__name__)

class VAPIClient:
    def __init__(self):
        self.api_key = os.getenv("VAPI_API_KEY")
        self.assistant_id = os.getenv("VAPI_ASSISTANT_ID")
        self.base_url = os.getenv("VAPI_BASE_URL", "https://api.vapi.ai")
        self.ghl_client = GHLClient()
        self.smart_links = SmartLink()
        self.frontend_base_url = os.getenv("FRONTEND_BASE_URL", "https://ai-iq-frontend.vercel.app")
        
        if not self.api_key or not self.assistant_id:
            logger.warning("VAPI API credentials not configured. VAPI integration will be disabled.")
            self.enabled = False
        else:
            self.enabled = True
    
    @property
    def headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def process_vapi_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming VAPI webhook with create_json_output tool results"""
        try:
            contact_info = webhook_data.get("contact_info", {})
            email = contact_info.get("email")
            name = contact_info.get("name")
            phone = contact_info.get("phone")
            
            if not email or not name:
                raise ValueError("Missing required contact information")
            
            contact_id = contact_result.get("contact", {}).get("id")
            smart_link = self.smart_links.generate_link(contact_id, self.frontend_base_url)
            
            ghl_custom_fields = self.format_vapi_results_for_ghl(webhook_data, smart_link)
            contact_result = await self.ghl_client.create_or_update_contact(
                email=email,
                name=name,
                mobile=phone or "",
                custom_fields=ghl_custom_fields
            )
            
            test_result = self.convert_vapi_to_test_result(webhook_data, email, name)
            
            return {
                "status": "success",
                "contact_id": contact_result.get("contact", {}).get("id"),
                "test_result": test_result,
                "ghl_fields_updated": len(ghl_custom_fields)
            }
            
        except Exception as e:
            logger.error(f"Error processing VAPI webhook: {e}")
            raise
    
    def convert_vapi_to_test_result(
        self, 
        vapi_data: Dict[str, Any], 
        email: str, 
        name: str
    ) -> DynamicTestResult:
        """Convert create_json_output tool results to internal DynamicTestResult format"""
        
        pain_points_data = vapi_data.get("pain_points", {})
        pain_points = {}
        
        pain_point_mapping = {
            "cant_scale_without_burnout": "cant_scale",
            "invisible_in_attention_landscape": "invisible_attention", 
            "outgunned_by_ai_competitors": "outgunned_competitors",
            "tech_gap_underusing_ai": "tech_gap"
        }
        
        for vapi_key, internal_key in pain_point_mapping.items():
            if vapi_key in pain_points_data:
                pp_data = pain_points_data[vapi_key]
                pain_points[internal_key] = PainPoint(
                    score=pp_data.get("score", 0),
                    description=pp_data.get("description", ""),
                    severity=SeverityLevel(pp_data.get("severity", "medium")),
                    recommendations=pp_data.get("evidence", []),
                    impact_areas=pp_data.get("impact_areas", [])
                )
        
        categories_data = vapi_data.get("categories", {})
        categories = {}
        
        category_mapping = {
            "website_form_function": "website",
            "social_media_effectiveness": "social_media",
            "digital_presence": "digital_presence", 
            "communication": "communication",
            "marketing": "marketing"
        }
        
        for vapi_key, internal_key in category_mapping.items():
            if vapi_key in categories_data:
                cat_data = categories_data[vapi_key]
                categories[internal_key] = Category(
                    score=cat_data.get("score", 0),
                    max_score=cat_data.get("max_score", 100),
                    percentage=cat_data.get("percentage", 0),
                    strengths=cat_data.get("strengths", []),
                    weaknesses=cat_data.get("weaknesses", []),
                    priority_actions=cat_data.get("priority_actions", [])
                )
        
        overall_data = vapi_data.get("overall_assessment", {})
        overall_score = overall_data.get("overall_score", 0)
        recommendations = overall_data.get("priority_recommendations", [])
        
        test_params = {}
        metadata = vapi_data.get("test_metadata", {})
        if metadata:
            test_params["call_duration"] = TestParameter(
                name="call_duration",
                value=metadata.get("call_duration", 0),
                category="metadata"
            )
            test_params["confidence_score"] = TestParameter(
                name="confidence_score", 
                value=metadata.get("confidence_score", 0),
                category="metadata"
            )
        
        return DynamicTestResult(
            user_id=email,  # Using email as user_id for now
            pain_points=pain_points,
            categories=categories,
            overall_score=overall_score,
            recommendations=recommendations,
            test_parameters=test_params,
            report_metadata={
                "source": "vapi",
                "ai_readiness_level": overall_data.get("ai_readiness_level", "beginner"),
                "custom_insights": vapi_data.get("custom_insights", {}),
                "contact_info": vapi_data.get("contact_info", {})
            },
            created_at=datetime.now()
        )
    
    def format_vapi_results_for_ghl(self, vapi_data: Dict[str, Any], smart_link: str) -> Dict[str, Any]:
        """Format create_json_output tool results for GHL custom fields"""
        ghl_fields = {}
        
        ghl_fields["ai_iq_test_results"] = json.dumps(vapi_data)
        
        overall_data = vapi_data.get("overall_assessment", {})
        ghl_fields["ai_iq_overall_score"] = overall_data.get("overall_score", 0)
        ghl_fields["ai_iq_readiness_level"] = overall_data.get("ai_readiness_level", "beginner")
        
        metadata = vapi_data.get("test_metadata", {})
        ghl_fields["ai_iq_test_date"] = metadata.get("completion_date", datetime.now().isoformat())
        ghl_fields["ai_iq_call_duration"] = metadata.get("call_duration", 0)
        ghl_fields["ai_iq_confidence_score"] = metadata.get("confidence_score", 0)
        
        pain_points = vapi_data.get("pain_points", {})
        ghl_fields["ai_iq_cant_scale_score"] = pain_points.get("cant_scale_without_burnout", {}).get("score", 0)
        ghl_fields["ai_iq_invisible_score"] = pain_points.get("invisible_in_attention_landscape", {}).get("score", 0)
        ghl_fields["ai_iq_outgunned_score"] = pain_points.get("outgunned_by_ai_competitors", {}).get("score", 0)
        ghl_fields["ai_iq_tech_gap_score"] = pain_points.get("tech_gap_underusing_ai", {}).get("score", 0)
        
        categories = vapi_data.get("categories", {})
        ghl_fields["ai_iq_website_score"] = categories.get("website_form_function", {}).get("score", 0)
        ghl_fields["ai_iq_social_score"] = categories.get("social_media_effectiveness", {}).get("score", 0)
        ghl_fields["ai_iq_digital_score"] = categories.get("digital_presence", {}).get("score", 0)
        ghl_fields["ai_iq_communication_score"] = categories.get("communication", {}).get("score", 0)
        ghl_fields["ai_iq_marketing_score"] = categories.get("marketing", {}).get("score", 0)
        
        ghl_fields["ai_iq_priority_actions"] = json.dumps(overall_data.get("priority_recommendations", []))
        ghl_fields["ai_iq_quick_wins"] = json.dumps(overall_data.get("quick_wins", []))
        ghl_fields["ai_iq_next_steps"] = json.dumps(overall_data.get("next_steps", []))
        ghl_fields["ai_iq_smart_link"] = smart_link
        
        return ghl_fields
    
    async def trigger_site_webhook(self, contact_id: str, test_result_data: Dict[str, Any], smart_link: str) -> bool:
        """Trigger webhook to notify site of new test results"""
        webhook_url = os.getenv("SITE_WEBHOOK_URL")
        if not webhook_url:
            logger.warning("Site webhook URL not configured")
            return False
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    webhook_url,
                    json={
                        "event_type": "vapi_test_completed",
                        "contact_id": contact_id,
                        "test_data": test_result_data,
                        "smart_link": smart_link,
                        "timestamp": datetime.now().isoformat()
                    },
                    headers={"Content-Type": "application/json"}
                )
                response.raise_for_status()
                return True
                
        except Exception as e:
            logger.error(f"Error triggering site webhook: {e}")
            return False
