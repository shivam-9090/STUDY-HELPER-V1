"""
Multi-provider AI service with intelligent fallback and rate limiting
"""
import time
import os
from typing import Optional, Dict, List, Callable, Any
from datetime import datetime
import google.generativeai as genai
from openai import OpenAI

class RateLimiter:
    """Track and enforce rate limits per provider"""
    
    def __init__(self):
        self.counters = {}  # {provider_key: {'count': 0, 'reset_at': timestamp}}
    
    def can_call(self, provider_key: str, limit_per_minute: int) -> bool:
        """Check if we can make a call within rate limit"""
        now = time.time()
        current_minute = int(now / 60)
        
        if provider_key not in self.counters:
            self.counters[provider_key] = {
                'count': 0,
                'minute': current_minute
            }
        
        counter = self.counters[provider_key]
        
        # Reset counter if new minute
        if counter['minute'] != current_minute:
            counter['count'] = 0
            counter['minute'] = current_minute
        
        # Check limit
        return counter['count'] < limit_per_minute
    
    def record_call(self, provider_key: str):
        """Record a successful API call"""
        now = time.time()
        current_minute = int(now / 60)
        
        if provider_key not in self.counters:
            self.counters[provider_key] = {
                'count': 0,
                'minute': current_minute
            }
        
        self.counters[provider_key]['count'] += 1
    
    def get_stats(self) -> Dict:
        """Get rate limit statistics"""
        now = time.time()
        current_minute = int(now / 60)
        
        stats = {}
        for key, data in self.counters.items():
            if data['minute'] == current_minute:
                stats[key] = {
                    'calls_this_minute': data['count'],
                    'active': True
                }
            else:
                stats[key] = {
                    'calls_this_minute': 0,
                    'active': False
                }
        
        return stats


class AIProvider:
    """Base class for AI providers"""
    
    def __init__(self, name: str, api_key: str, rate_limit: int, cost_per_1k: float = 0):
        self.name = name
        self.api_key = api_key
        self.rate_limit = rate_limit
        self.cost_per_1k = cost_per_1k
        self.failed_count = 0
        self.success_count = 0
        self.total_tokens = 0
    
    def can_use(self, rate_limiter: RateLimiter) -> bool:
        """Check if provider can be used"""
        if not self.api_key:
            return False
        if self.failed_count >= 5:  # Too many recent failures
            return False
        return rate_limiter.can_call(self.name, self.rate_limit)
    
    def call(self, prompt: str, **kwargs) -> str:
        """Make API call - to be implemented by subclasses"""
        raise NotImplementedError
    
    def record_success(self, rate_limiter: RateLimiter, tokens: int = 0):
        """Record successful call"""
        self.success_count += 1
        self.total_tokens += tokens
        self.failed_count = max(0, self.failed_count - 1)  # Reduce failure count
        rate_limiter.record_call(self.name)
    
    def record_failure(self):
        """Record failed call"""
        self.failed_count += 1
    
    def get_stats(self) -> Dict:
        """Get provider statistics"""
        return {
            'name': self.name,
            'success_count': self.success_count,
            'failed_count': self.failed_count,
            'total_tokens': self.total_tokens,
            'estimated_cost': (self.total_tokens / 1000) * self.cost_per_1k
        }


class GeminiProvider(AIProvider):
    """Google Gemini provider"""
    
    def __init__(self, api_key: str, provider_id: str = "gemini"):
        # Use provider_id to distinguish between multiple Gemini instances
        super().__init__(
            name=provider_id,
            api_key=api_key,
            rate_limit=14,  # Stay under 15/min
            cost_per_1k=0.0  # Free tier
        )
        # Store API key for later use (don't configure globally yet)
        self._api_key = api_key
        self.model = None
    
    def call(self, prompt: str, **kwargs) -> str:
        # Configure with this specific key right before calling
        if self._api_key:
            genai.configure(api_key=self._api_key)
            if not self.model:
                self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        response = self.model.generate_content(
            prompt,
            generation_config={
                'temperature': kwargs.get('temperature', 0.7),
                'max_output_tokens': kwargs.get('max_tokens', 1024),
            }
        )
        return response.text


class OpenAIProvider(AIProvider):
    """OpenAI GPT provider"""
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        super().__init__(
            name=f"openai-{model}",
            api_key=api_key,
            rate_limit=10,
            cost_per_1k=0.002  # GPT-3.5 pricing
        )
        self.model = model
        if api_key:
            self.client = OpenAI(api_key=api_key)
    
    def call(self, prompt: str, **kwargs) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert AI tutor for engineering students."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=kwargs.get('max_tokens', 1024),
            temperature=kwargs.get('temperature', 0.7)
        )
        return response.choices[0].message.content


class DeepSeekProvider(AIProvider):
    """DeepSeek provider"""
    
    def __init__(self, api_key: str):
        super().__init__(
            name="deepseek",
            api_key=api_key,
            rate_limit=10,
            cost_per_1k=0.0014  # DeepSeek pricing
        )
        if api_key:
            self.client = OpenAI(
                api_key=api_key,
                base_url="https://api.deepseek.com"
            )
    
    def call(self, prompt: str, **kwargs) -> str:
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are an expert AI tutor for engineering students."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=kwargs.get('max_tokens', 1024),
            temperature=kwargs.get('temperature', 0.7)
        )
        return response.choices[0].message.content


class ProviderManager:
    """Manages multiple AI providers with intelligent fallback"""
    
    def __init__(self):
        self.rate_limiter = RateLimiter()
        self.providers: List[AIProvider] = []
        self._initialize_providers()
    
    def _initialize_providers(self):
        """Initialize all available providers"""
        # Gemini providers (multiple keys with unique IDs)
        gemini_key = os.getenv('AI_API_KEY', '')
        if gemini_key:
            self.providers.append(GeminiProvider(gemini_key, "gemini-primary"))
        
        gemini_backup = os.getenv('AI_API_KEY_BACKUP', '')
        if gemini_backup:
            self.providers.append(GeminiProvider(gemini_backup, "gemini-backup"))
        
        # OpenAI
        openai_key = os.getenv('OPENAI_API_KEY', '')
        if openai_key:
            self.providers.append(OpenAIProvider(openai_key))
        
        # DeepSeek
        deepseek_key = os.getenv('DEEPSEEK_API_KEY', '')
        if deepseek_key:
            self.providers.append(DeepSeekProvider(deepseek_key))
        
        print(f"✅ Initialized {len(self.providers)} AI provider(s)")
    
    def call_with_fallback(self, prompt: str, **kwargs) -> Optional[str]:
        """Call AI with automatic fallback across providers"""
        errors = []
        
        for provider in self.providers:
            if not provider.can_use(self.rate_limiter):
                print(f"⏭️ Skipping {provider.name} (rate limit or failures)")
                continue
            
            try:
                print(f"🔄 Trying {provider.name}...")
                result = provider.call(prompt, **kwargs)
                
                if result:
                    provider.record_success(self.rate_limiter, len(result))
                    print(f"✅ Success with {provider.name}")
                    return result
            
            except Exception as e:
                error_msg = str(e)
                errors.append(f"{provider.name}: {error_msg}")
                provider.record_failure()
                
                # Check if quota error - skip this provider
                if "429" in error_msg or "quota" in error_msg.lower() or "insufficient" in error_msg.lower():
                    print(f"❌ {provider.name} quota exceeded, trying next...")
                    continue
                else:
                    print(f"❌ {provider.name} error: {error_msg}")
        
        # All providers failed
        print(f"❌ All providers failed. Errors: {errors}")
        return None
    
    def get_stats(self) -> Dict:
        """Get statistics for all providers"""
        return {
            'providers': [p.get_stats() for p in self.providers],
            'rate_limits': self.rate_limiter.get_stats()
        }


# Global provider manager
provider_manager = ProviderManager()
