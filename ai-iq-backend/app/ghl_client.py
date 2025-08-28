import httpx
import os
from typing import Dict, Any, Optional, List
import json
import logging
from .models import GHLContact, TestParameter

logger = logging.getLogger(__name__)

class GHLClient:
    def __init__(self):
        self.api_key = os.getenv("GHL_API_KEY")
        self.location_id = os.getenv("GHL_LOCATION_ID")
        self.base_url = os.getenv("GHL_BASE_URL", "https://services.leadconnectorhq.com")
        
        if not self.api_key or not self.location_id:
            logger.warning("GHL API credentials not configured. GHL integration will be disabled.")
            self.enabled = False
        else:
            self.enabled = True
    
    @property
    def headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Version": "2021-07-28"
        }
    
    async def create_or_update_contact(
        self, 
        email: str, 
        name: str, 
        mobile: str, 
        custom_fields: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Create or update a contact in GHL"""
        if not self.enabled:
            return {"contact": {"id": "mock_contact_id"}}
        
        try:
            async with httpx.AsyncClient() as client:
                existing_contact = await self.get_contact_by_email(email)
                
                contact_data = {
                    "email": email,
                    "name": name,
                    "phone": mobile,
                    "locationId": self.location_id
                }
                
                if custom_fields:
                    contact_data["customFields"] = custom_fields
                
                if existing_contact:
                    contact_id = existing_contact["id"]
                    response = await client.put(
                        f"{self.base_url}/contacts/{contact_id}",
                        headers=self.headers,
                        json=contact_data
                    )
                else:
                    response = await client.post(
                        f"{self.base_url}/contacts",
                        headers=self.headers,
                        json=contact_data
                    )
                
                response.raise_for_status()
                return response.json()
                
        except Exception as e:
            logger.error(f"Error creating/updating GHL contact: {e}")
            return {"contact": {"id": "error_contact_id"}}
    
    async def get_contact_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Retrieve contact from GHL by email"""
        if not self.enabled:
            return None
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/contacts/search",
                    headers=self.headers,
                    params={"email": email, "locationId": self.location_id}
                )
                response.raise_for_status()
                data = response.json()
                
                if data.get("contacts") and len(data["contacts"]) > 0:
                    return data["contacts"][0]
                return None
                
        except Exception as e:
            logger.error(f"Error fetching GHL contact: {e}")
            return None
    
    async def update_contact_custom_fields(
        self, 
        contact_id: str, 
        custom_fields: Dict[str, Any]
    ) -> bool:
        """Update custom fields for a contact"""
        if not self.enabled:
            return True
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.put(
                    f"{self.base_url}/contacts/{contact_id}",
                    headers=self.headers,
                    json={"customFields": custom_fields}
                )
                response.raise_for_status()
                return True
                
        except Exception as e:
            logger.error(f"Error updating GHL contact custom fields: {e}")
            return False
    
    async def add_contact_to_workflow(
        self, 
        contact_id: str, 
        workflow_id: str
    ) -> bool:
        """Add contact to a GHL workflow"""
        if not self.enabled:
            return True
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/workflows/{workflow_id}/subscribe",
                    headers=self.headers,
                    json={"contactId": contact_id}
                )
                response.raise_for_status()
                return True
                
        except Exception as e:
            logger.error(f"Error adding contact to GHL workflow: {e}")
            return False
    
    def extract_test_parameters_from_contact(
        self, 
        contact_data: Dict[str, Any]
    ) -> Dict[str, TestParameter]:
        """Extract test parameters from GHL contact custom fields"""
        parameters = {}
        custom_fields = contact_data.get("customFields", {})
        
        parameter_mappings = {
            "industry": {"weight": 1.2, "category": "business"},
            "company_size": {"weight": 1.1, "category": "business"},
            "current_ai_usage": {"weight": 1.5, "category": "technology"},
            "primary_challenges": {"weight": 1.3, "category": "pain_points"},
            "budget_range": {"weight": 1.0, "category": "business"},
            "tech_expertise": {"weight": 1.2, "category": "technology"}
        }
        
        for field_name, config in parameter_mappings.items():
            if field_name in custom_fields:
                parameters[field_name] = TestParameter(
                    name=field_name,
                    value=custom_fields[field_name],
                    weight=config["weight"],
                    category=config["category"]
                )
        
        return parameters
    
    def format_test_results_for_ghl(
        self, 
        test_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Format test results for storage in GHL custom fields"""
        ghl_fields = {
            "ai_iq_overall_score": test_result["overall_score"],
            "ai_iq_test_date": test_result["created_at"].isoformat() if hasattr(test_result["created_at"], "isoformat") else str(test_result["created_at"]),
            "ai_iq_report_json": json.dumps({
                "pain_points": test_result["pain_points"],
                "categories": test_result["categories"],
                "recommendations": test_result["recommendations"]
            })
        }
        
        for pain_point_key, pain_point_data in test_result["pain_points"].items():
            field_name = f"ai_iq_{pain_point_key}_score"
            if isinstance(pain_point_data, dict) and "score" in pain_point_data:
                ghl_fields[field_name] = pain_point_data["score"]
        
        for category_key, category_data in test_result["categories"].items():
            field_name = f"ai_iq_{category_key}_score"
            if isinstance(category_data, dict) and "score" in category_data:
                ghl_fields[field_name] = category_data["score"]
        
        return ghl_fields
