"""
Smart caching system for AI responses
Avoids repeated API calls for same prompts
"""
import json
import hashlib
import os
import time
from pathlib import Path
from functools import wraps
from typing import Optional, Any, Dict

class ResponseCache:
    """File-based cache for AI responses"""
    
    def __init__(self, cache_dir: str = "cache", default_ttl: int = 3600):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.default_ttl = default_ttl
        
    def _get_cache_key(self, prompt: str, metadata: Dict = None) -> str:
        """Generate unique cache key from prompt + metadata"""
        cache_input = prompt + json.dumps(metadata or {}, sort_keys=True)
        return hashlib.sha256(cache_input.encode()).hexdigest()
    
    def _get_cache_path(self, key: str) -> Path:
        """Get file path for cache key"""
        return self.cache_dir / f"{key}.json"
    
    def get(self, prompt: str, metadata: Dict = None) -> Optional[Any]:
        """Retrieve cached response if exists and not expired"""
        key = self._get_cache_key(prompt, metadata)
        cache_file = self._get_cache_path(key)
        
        if not cache_file.exists():
            return None
        
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Check if expired
            if time.time() > data.get('expires_at', 0):
                cache_file.unlink()  # Delete expired cache
                return None
            
            return data.get('response')
        except Exception as e:
            print(f"⚠️ Cache read error: {e}")
            return None
    
    def set(self, prompt: str, response: Any, metadata: Dict = None, ttl: int = None):
        """Store response in cache"""
        key = self._get_cache_key(prompt, metadata)
        cache_file = self._get_cache_path(key)
        
        ttl = ttl or self.default_ttl
        data = {
            'prompt': prompt[:100],  # Store truncated prompt for debugging
            'response': response,
            'metadata': metadata,
            'cached_at': time.time(),
            'expires_at': time.time() + ttl
        }
        
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ Cache write error: {e}")
    
    def clear_expired(self):
        """Clean up expired cache files"""
        now = time.time()
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                with open(cache_file, 'r') as f:
                    data = json.load(f)
                if now > data.get('expires_at', 0):
                    cache_file.unlink()
            except Exception:
                pass
    
    def stats(self) -> Dict:
        """Get cache statistics"""
        total = 0
        valid = 0
        expired = 0
        now = time.time()
        
        for cache_file in self.cache_dir.glob("*.json"):
            total += 1
            try:
                with open(cache_file, 'r') as f:
                    data = json.load(f)
                if now > data.get('expires_at', 0):
                    expired += 1
                else:
                    valid += 1
            except Exception:
                pass
        
        return {
            'total_files': total,
            'valid': valid,
            'expired': expired,
            'cache_dir': str(self.cache_dir)
        }


def cached_response(ttl: int = 3600):
    """Decorator for caching function responses"""
    cache = ResponseCache(default_ttl=ttl)
    
    def decorator(func):
        @wraps(func)
        def wrapper(prompt: str, *args, **kwargs):
            # Create metadata from kwargs for cache key
            metadata = {
                'subject': kwargs.get('subject'),
                'level': kwargs.get('level'),
                'topic': kwargs.get('topic')
            }
            
            # Try to get from cache
            cached = cache.get(prompt, metadata)
            if cached:
                print(f"✅ Cache HIT: {prompt[:50]}...")
                return cached
            
            # Call function and cache result
            print(f"🔍 Cache MISS: Calling AI API...")
            result = func(prompt, *args, **kwargs)
            
            if result:
                cache.set(prompt, result, metadata, ttl)
            
            return result
        
        return wrapper
    return decorator


# Global cache instance
response_cache = ResponseCache()
