#!/usr/bin/env python3
"""
API Key Manager for Abhishek Ambi's Portfolio Chatbot
Handles secure API key generation, validation, and management.
"""

import secrets
import hashlib
import json
import os
from datetime import datetime, timedelta
from typing import Dict, Optional, List
from dataclasses import dataclass, asdict

@dataclass
class APIKey:
    """API Key data structure."""
    key_id: str
    key_hash: str
    name: str
    description: str
    created_at: str
    expires_at: Optional[str]
    is_active: bool
    permissions: List[str]
    usage_count: int
    last_used: Optional[str]

class APIKeyManager:
    """
    Manages API keys for the portfolio chatbot.
    Provides secure key generation, validation, and tracking.
    """
    
    def __init__(self, keys_file: str = "api_keys.json"):
        """
        Initialize the API key manager.
        
        Args:
            keys_file: Path to the JSON file storing API keys
        """
        self.keys_file = keys_file
        self.keys: Dict[str, APIKey] = {}
        self.load_keys()
    
    def generate_api_key(self, name: str, description: str = "", 
                        expires_in_days: Optional[int] = None,
                        permissions: Optional[List[str]] = None) -> str:
        """
        Generate a new API key.
        
        Args:
            name: Name for the API key
            description: Description of the key's purpose
            expires_in_days: Days until key expires (None for no expiration)
            permissions: List of permissions for this key
            
        Returns:
            The generated API key (only shown once)
        """
        # Generate a secure random key
        api_key = f"abhishek_{secrets.token_urlsafe(32)}"
        
        # Create key ID and hash
        key_id = secrets.token_hex(16)
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        
        # Set expiration
        created_at = datetime.now().isoformat()
        expires_at = None
        if expires_in_days:
            expires_at = (datetime.now() + timedelta(days=expires_in_days)).isoformat()
        
        # Set default permissions
        if permissions is None:
            permissions = ["chat", "projects", "skills", "recommendations"]
        
        # Create API key object
        api_key_obj = APIKey(
            key_id=key_id,
            key_hash=key_hash,
            name=name,
            description=description,
            created_at=created_at,
            expires_at=expires_at,
            is_active=True,
            permissions=permissions,
            usage_count=0,
            last_used=None
        )
        
        # Store the key
        self.keys[key_hash] = api_key_obj
        self.save_keys()
        
        return api_key
    
    def validate_api_key(self, api_key: str) -> Optional[APIKey]:
        """
        Validate an API key.
        
        Args:
            api_key: The API key to validate
            
        Returns:
            APIKey object if valid, None otherwise
        """
        if not api_key:
            return None
        
        # Hash the provided key
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        
        # Check if key exists
        if key_hash not in self.keys:
            return None
        
        api_key_obj = self.keys[key_hash]
        
        # Check if key is active
        if not api_key_obj.is_active:
            return None
        
        # Check if key has expired
        if api_key_obj.expires_at:
            expires_at = datetime.fromisoformat(api_key_obj.expires_at)
            if datetime.now() > expires_at:
                return None
        
        # Update usage statistics
        api_key_obj.usage_count += 1
        api_key_obj.last_used = datetime.now().isoformat()
        self.save_keys()
        
        return api_key_obj
    
    def has_permission(self, api_key: str, permission: str) -> bool:
        """
        Check if an API key has a specific permission.
        
        Args:
            api_key: The API key to check
            permission: The permission to check for
            
        Returns:
            True if key has permission, False otherwise
        """
        api_key_obj = self.validate_api_key(api_key)
        if not api_key_obj:
            return False
        
        return permission in api_key_obj.permissions
    
    def revoke_api_key(self, api_key: str) -> bool:
        """
        Revoke an API key.
        
        Args:
            api_key: The API key to revoke
            
        Returns:
            True if key was revoked, False if not found
        """
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        
        if key_hash in self.keys:
            self.keys[key_hash].is_active = False
            self.save_keys()
            return True
        
        return False
    
    def list_api_keys(self) -> List[Dict]:
        """
        List all API keys (without the actual key values).
        
        Returns:
            List of API key information
        """
        return [
            {
                "key_id": key.key_id,
                "name": key.name,
                "description": key.description,
                "created_at": key.created_at,
                "expires_at": key.expires_at,
                "is_active": key.is_active,
                "permissions": key.permissions,
                "usage_count": key.usage_count,
                "last_used": key.last_used
            }
            for key in self.keys.values()
        ]
    
    def get_api_key_stats(self) -> Dict:
        """
        Get statistics about API keys.
        
        Returns:
            Dictionary with API key statistics
        """
        total_keys = len(self.keys)
        active_keys = sum(1 for key in self.keys.values() if key.is_active)
        expired_keys = sum(1 for key in self.keys.values() 
                          if key.expires_at and datetime.now() > datetime.fromisoformat(key.expires_at))
        total_usage = sum(key.usage_count for key in self.keys.values())
        
        return {
            "total_keys": total_keys,
            "active_keys": active_keys,
            "expired_keys": expired_keys,
            "total_usage": total_usage
        }
    
    def load_keys(self):
        """Load API keys from file."""
        if os.path.exists(self.keys_file):
            try:
                with open(self.keys_file, 'r') as f:
                    data = json.load(f)
                    self.keys = {}
                    for key_hash, key_data in data.items():
                        self.keys[key_hash] = APIKey(**key_data)
            except Exception as e:
                print(f"Warning: Could not load API keys: {e}")
                self.keys = {}
        else:
            self.keys = {}
    
    def save_keys(self):
        """Save API keys to file."""
        try:
            with open(self.keys_file, 'w') as f:
                data = {key_hash: asdict(key_obj) for key_hash, key_obj in self.keys.items()}
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving API keys: {e}")


def create_initial_api_key():
    """Create an initial API key for testing."""
    manager = APIKeyManager()
    
    # Create a default API key
    api_key = manager.generate_api_key(
        name="Default API Key",
        description="Default API key for Abhishek Ambi's Portfolio Chatbot",
        expires_in_days=365,  # Expires in 1 year
        permissions=["chat", "projects", "skills", "recommendations"]
    )
    
    print("🔑 Initial API Key Generated!")
    print("=" * 50)
    print(f"API Key: {api_key}")
    print("=" * 50)
    print("⚠️  IMPORTANT: Save this key securely - it won't be shown again!")
    print("📝 Use this key in your API requests with the header:")
    print("   X-API-Key: your_api_key_here")
    
    return api_key


if __name__ == "__main__":
    # Create initial API key
    create_initial_api_key() 