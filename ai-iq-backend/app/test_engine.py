import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
import random
from .models import (
    DynamicTestResult, PainPoint, Category, DynamicSection, 
    TestParameter, SeverityLevel, SectionType, ConfigurationSettings
)

class AIIQTestEngine:
    def __init__(self, config_path: Optional[str] = None):
        self.config = self._load_configuration(config_path)
        self.pain_point_definitions = self._get_pain_point_definitions()
        self.category_definitions = self._get_category_definitions()
    
    def _load_configuration(self, config_path: Optional[str] = None) -> ConfigurationSettings:
        """Load configuration from file or use defaults"""
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    config_data = json.load(f)
                return ConfigurationSettings(**config_data)
            except Exception:
                pass
        
        return ConfigurationSettings(
            pain_point_weights={
                "cant_scale_without_burnout": 1.3,
                "invisible_attention_landscape": 1.1,
                "outgunned_by_competitors": 1.4,
                "tech_gap_ai_advantages": 1.2
            },
            category_weights={
                "website_form_function": 1.0,
                "social_media_effectiveness": 1.1,
                "digital_presence": 1.2,
                "communication": 1.0,
                "marketing": 1.3
            },
            scoring_thresholds={
                "low": 30,
                "medium": 60,
                "high": 80,
                "excellent": 90
            }
        )
    
    def _get_pain_point_definitions(self) -> Dict[str, Dict[str, Any]]:
        """Define pain point templates and scoring logic"""
        return {
            "cant_scale_without_burnout": {
                "title": "Can't Scale Without Burning Out",
                "base_score_range": (5, 9),
                "severity_thresholds": {"low": 3, "medium": 6, "high": 8},
                "recommendations": [
                    "Implement AI-powered task automation",
                    "Create standard operating procedures",
                    "Deploy intelligent workflow management",
                    "Establish automated delegation systems"
                ],
                "impact_areas": ["productivity", "team_management", "operations"]
            },
            "invisible_attention_landscape": {
                "title": "Invisible in the New Attention Landscape",
                "base_score_range": (4, 8),
                "severity_thresholds": {"low": 3, "medium": 5, "high": 7},
                "recommendations": [
                    "Optimize SEO strategy with AI tools",
                    "Increase social media presence",
                    "Implement content automation",
                    "Deploy AI-powered audience targeting"
                ],
                "impact_areas": ["visibility", "marketing", "brand_awareness"]
            },
            "outgunned_by_competitors": {
                "title": "Outgunned by AI-Enabled Competitors",
                "base_score_range": (6, 9),
                "severity_thresholds": {"low": 4, "medium": 7, "high": 8},
                "recommendations": [
                    "Adopt AI-powered analytics",
                    "Implement chatbot solutions",
                    "Deploy competitive intelligence tools",
                    "Automate customer insights gathering"
                ],
                "impact_areas": ["competitive_advantage", "technology", "market_position"]
            },
            "tech_gap_ai_advantages": {
                "title": "Tech Gap: Underusing AI's Unfair Advantages",
                "base_score_range": (5, 8),
                "severity_thresholds": {"low": 3, "medium": 6, "high": 7},
                "recommendations": [
                    "AI training for team",
                    "Implement AI workflow automation",
                    "Deploy predictive analytics",
                    "Integrate AI decision support systems"
                ],
                "impact_areas": ["technology_adoption", "efficiency", "innovation"]
            }
        }
    
    def _get_category_definitions(self) -> Dict[str, Dict[str, Any]]:
        """Define category templates and scoring logic"""
        return {
            "website_form_function": {
                "title": "Website Form and Function",
                "max_score": 40,
                "strengths_pool": [
                    "Good mobile responsiveness",
                    "Fast loading times",
                    "Clean design",
                    "User-friendly navigation",
                    "Strong SEO foundation"
                ],
                "weaknesses_pool": [
                    "Poor conversion optimization",
                    "Limited AI integration",
                    "Outdated content management",
                    "Lack of personalization",
                    "Missing analytics tracking"
                ],
                "priority_actions_pool": [
                    "Add AI chatbot",
                    "Implement dynamic personalization",
                    "Optimize conversion funnels",
                    "Deploy A/B testing automation",
                    "Integrate predictive analytics"
                ]
            },
            "social_media_effectiveness": {
                "title": "Social Media Effectiveness",
                "max_score": 40,
                "strengths_pool": [
                    "Consistent posting",
                    "Good engagement rates",
                    "Strong visual content",
                    "Active community management",
                    "Cross-platform presence"
                ],
                "weaknesses_pool": [
                    "Limited automation",
                    "No AI content generation",
                    "Poor audience targeting",
                    "Inconsistent messaging",
                    "Lack of performance analytics"
                ],
                "priority_actions_pool": [
                    "Implement AI content creation",
                    "Automate posting schedules",
                    "Deploy audience intelligence",
                    "Optimize engagement algorithms",
                    "Integrate social listening tools"
                ]
            },
            "digital_presence": {
                "title": "Digital Presence",
                "max_score": 40,
                "strengths_pool": [
                    "Strong brand recognition",
                    "Good online reviews",
                    "Consistent branding",
                    "Multi-channel presence",
                    "Quality content creation"
                ],
                "weaknesses_pool": [
                    "Limited SEO optimization",
                    "No AI-powered insights",
                    "Poor local search presence",
                    "Inconsistent messaging",
                    "Lack of reputation management"
                ],
                "priority_actions_pool": [
                    "AI-powered SEO optimization",
                    "Implement analytics automation",
                    "Deploy reputation monitoring",
                    "Optimize local search presence",
                    "Integrate omnichannel tracking"
                ]
            },
            "communication": {
                "title": "Communication",
                "max_score": 40,
                "strengths_pool": [
                    "Clear messaging",
                    "Good customer service",
                    "Responsive support",
                    "Professional communication",
                    "Multi-channel availability"
                ],
                "weaknesses_pool": [
                    "Manual processes",
                    "No AI assistance",
                    "Slow response times",
                    "Inconsistent messaging",
                    "Limited personalization"
                ],
                "priority_actions_pool": [
                    "Deploy AI customer service",
                    "Automate follow-up sequences",
                    "Implement smart routing",
                    "Optimize response templates",
                    "Integrate sentiment analysis"
                ]
            },
            "marketing": {
                "title": "Marketing",
                "max_score": 40,
                "strengths_pool": [
                    "Good targeting",
                    "Strong campaigns",
                    "Creative content",
                    "Multi-channel approach",
                    "Brand consistency"
                ],
                "weaknesses_pool": [
                    "Limited personalization",
                    "Manual optimization",
                    "Poor attribution tracking",
                    "Inconsistent messaging",
                    "Lack of predictive insights"
                ],
                "priority_actions_pool": [
                    "AI-powered personalization",
                    "Automated A/B testing",
                    "Deploy predictive analytics",
                    "Implement attribution modeling",
                    "Optimize campaign automation"
                ]
            }
        }
    
    def generate_dynamic_test_result(
        self, 
        user_id: str, 
        test_parameters: Optional[Dict[str, TestParameter]] = None,
        ghl_contact_data: Optional[Dict[str, Any]] = None
    ) -> DynamicTestResult:
        """Generate a dynamic test result based on parameters"""
        
        pain_points = self._generate_pain_points(test_parameters, ghl_contact_data)
        categories = self._generate_categories(test_parameters, ghl_contact_data)
        overall_score = self._calculate_overall_score(pain_points, categories)
        recommendations = self._generate_recommendations(pain_points, categories)
        custom_sections = self._generate_custom_sections(test_parameters)
        
        return DynamicTestResult(
            user_id=user_id,
            pain_points=pain_points,
            categories=categories,
            overall_score=overall_score,
            recommendations=recommendations,
            custom_sections=custom_sections,
            test_parameters=test_parameters,
            report_metadata={
                "generation_method": "dynamic",
                "parameter_count": len(test_parameters) if test_parameters else 0,
                "has_ghl_data": bool(ghl_contact_data),
                "sections_count": len(custom_sections) if custom_sections else 0
            },
            created_at=datetime.now()
        )
    
    def _generate_pain_points(
        self, 
        test_parameters: Optional[Dict[str, TestParameter]] = None,
        ghl_contact_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, PainPoint]:
        """Generate pain points with dynamic scoring"""
        pain_points = {}
        
        for key, definition in self.pain_point_definitions.items():
            base_min, base_max = definition["base_score_range"]
            
            weight = self.config.pain_point_weights.get(key, 1.0)
            if test_parameters:
                weight *= self._calculate_parameter_influence(test_parameters, definition["impact_areas"])
            
            score = int(random.uniform(base_min, base_max) * weight)
            score = max(1, min(10, score))
            
            severity = self._determine_severity(score, definition["severity_thresholds"])
            
            pain_points[key] = PainPoint(
                score=score,
                description=self._generate_dynamic_description(key, score, test_parameters),
                severity=severity,
                recommendations=random.sample(definition["recommendations"], min(2, len(definition["recommendations"]))),
                impact_areas=definition["impact_areas"]
            )
        
        return pain_points
    
    def _generate_categories(
        self, 
        test_parameters: Optional[Dict[str, TestParameter]] = None,
        ghl_contact_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Category]:
        """Generate categories with dynamic scoring"""
        categories = {}
        
        for key, definition in self.category_definitions.items():
            max_score = definition["max_score"]
            
            weight = self.config.category_weights.get(key, 1.0)
            if test_parameters:
                weight *= self._calculate_parameter_influence(test_parameters, [key])
            
            base_score = random.uniform(20, 35)
            score = int(base_score * weight)
            score = max(10, min(max_score, score))
            
            percentage = int((score / max_score) * 100)
            
            strengths = random.sample(definition["strengths_pool"], random.randint(2, 3))
            weaknesses = random.sample(definition["weaknesses_pool"], random.randint(2, 3))
            priority_actions = random.sample(definition["priority_actions_pool"], random.randint(2, 3))
            
            categories[key] = Category(
                score=score,
                max_score=max_score,
                percentage=percentage,
                strengths=strengths,
                weaknesses=weaknesses,
                priority_actions=priority_actions
            )
        
        return categories
    
    def _generate_custom_sections(
        self, 
        test_parameters: Optional[Dict[str, TestParameter]] = None
    ) -> Optional[Dict[str, DynamicSection]]:
        """Generate custom sections based on parameters"""
        if not test_parameters or not self.config.dynamic_sections_enabled:
            return None
        
        custom_sections = {}
        
        if "industry" in test_parameters:
            industry = test_parameters["industry"].value
            custom_sections["industry_specific"] = DynamicSection(
                title=f"{industry} Industry Insights",
                content={
                    "industry_trends": f"AI adoption trends specific to {industry}",
                    "competitive_landscape": f"Key AI opportunities in {industry}",
                    "recommendations": [
                        f"Industry-specific AI tools for {industry}",
                        f"Best practices from {industry} leaders"
                    ]
                },
                display_order=10,
                section_type=SectionType.CUSTOM,
                is_expandable=True
            )
        
        if "company_size" in test_parameters:
            size = test_parameters["company_size"].value
            custom_sections["size_specific"] = DynamicSection(
                title=f"{size} Company Recommendations",
                content={
                    "scaling_strategies": f"AI scaling strategies for {size} companies",
                    "resource_allocation": f"Optimal AI investment for {size} businesses",
                    "implementation_timeline": f"Recommended AI adoption timeline for {size} companies"
                },
                display_order=11,
                section_type=SectionType.CUSTOM,
                is_expandable=True
            )
        
        return custom_sections if custom_sections else None
    
    def _calculate_parameter_influence(
        self, 
        test_parameters: Dict[str, TestParameter], 
        impact_areas: List[str]
    ) -> float:
        """Calculate how parameters influence scoring"""
        influence = 1.0
        
        for param in test_parameters.values():
            if param.category in impact_areas or any(area in str(param.value).lower() for area in impact_areas):
                influence *= param.weight
        
        return min(1.5, max(0.7, influence))
    
    def _determine_severity(self, score: int, thresholds: Dict[str, int]) -> SeverityLevel:
        """Determine severity level based on score"""
        if score <= thresholds["low"]:
            return SeverityLevel.LOW
        elif score <= thresholds["medium"]:
            return SeverityLevel.MEDIUM
        elif score <= thresholds["high"]:
            return SeverityLevel.HIGH
        else:
            return SeverityLevel.CRITICAL
    
    def _generate_dynamic_description(
        self, 
        pain_point_key: str, 
        score: int, 
        test_parameters: Optional[Dict[str, TestParameter]] = None
    ) -> str:
        """Generate dynamic descriptions based on score and parameters"""
        base_descriptions = {
            "cant_scale_without_burnout": "Struggling with delegation and automation",
            "invisible_attention_landscape": "Limited visibility in digital channels",
            "outgunned_by_competitors": "Competitors using advanced AI tools",
            "tech_gap_ai_advantages": "Underutilizing available AI technologies"
        }
        
        base = base_descriptions.get(pain_point_key, "AI optimization opportunity identified")
        
        if test_parameters and "industry" in test_parameters:
            industry = test_parameters["industry"].value
            base += f" in the {industry} sector"
        
        if score >= 8:
            base += " - requires immediate attention"
        elif score >= 6:
            base += " - significant improvement opportunity"
        else:
            base += " - moderate optimization potential"
        
        return base
    
    def _calculate_overall_score(
        self, 
        pain_points: Dict[str, PainPoint], 
        categories: Dict[str, Category]
    ) -> int:
        """Calculate overall AI IQ score"""
        category_total = sum(cat.score for cat in categories.values())
        pain_point_penalty = sum(pp.score for pp in pain_points.values()) * 2
        
        base_score = category_total - pain_point_penalty
        return max(50, min(200, base_score))
    
    def _generate_recommendations(
        self, 
        pain_points: Dict[str, PainPoint], 
        categories: Dict[str, Category]
    ) -> List[str]:
        """Generate comprehensive recommendations"""
        recommendations = [
            "Implement comprehensive AI automation strategy",
            "Focus on high-impact areas: scaling and competitor analysis",
            "Prioritize AI integration in customer-facing processes",
            "Develop team AI literacy and capabilities"
        ]
        
        high_severity_pain_points = [
            pp for pp in pain_points.values() 
            if pp.severity in [SeverityLevel.HIGH, SeverityLevel.CRITICAL]
        ]
        
        if high_severity_pain_points:
            recommendations.insert(0, "Address critical pain points immediately for maximum impact")
        
        low_scoring_categories = [
            cat for cat in categories.values() 
            if cat.percentage < 70
        ]
        
        if low_scoring_categories:
            recommendations.append("Focus improvement efforts on underperforming categories")
        
        return recommendations
