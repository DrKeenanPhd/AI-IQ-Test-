import hmac
import hashlib
import time
import os
from typing import Optional, Dict, Any

class SmartLink:
    """Generate and validate secure smart links for direct access to test results"""
    
    def __init__(self):
        self.secret = os.getenv("SMART_LINK_SECRET", "default-dev-secret-change-in-production")
        self.ttl_seconds = int(os.getenv("SMART_LINK_TTL_SECONDS", "259200"))  # default 72h
    
    def sign(self, contact_id: str, expires: int) -> str:
        """Generate HMAC signature for contact_id and expiry timestamp"""
        msg = f"{contact_id}:{expires}".encode()
        return hmac.new(self.secret.encode(), msg, hashlib.sha256).hexdigest()[:32]
    
    def validate(self, contact_id: str, expires: str, sig: str) -> bool:
        """Validate smart link signature and expiration"""
        try:
            exp = int(expires)
        except ValueError:
            return False
        
        if time.time() > exp:  # expired
            return False
        
        expected = self.sign(contact_id, exp)
        return hmac.compare_digest(expected, sig)
    
    def generate_link(self, contact_id: str, base_url: str) -> str:
        """Generate a complete smart link URL"""
        expires = int(time.time()) + self.ttl_seconds
        sig = self.sign(contact_id, expires)
        return f"{base_url}?contact_id={contact_id}&expires={expires}&sig={sig}"
    
    @staticmethod
    def find_user_by_contact_id(contact_id: str, users_db: Dict[str, Any]) -> Optional[str]:
        """Find user_id by ghl_contact_id using database iteration pattern"""
        for user_id, user in users_db.items():
            if user.get("ghl_contact_id") == contact_id:
                return user_id
        return None
