"""
Optimized AI Service with caching, local FAQs, and multi-provider fallback
UNLIMITED FREE USAGE through smart optimizations!
"""
import os
import sys
from typing import Optional

# Add utils to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.cache import response_cache, cached_response
from utils.local_faq import faq_handler
from utils.provider_manager import provider_manager
from utils.prompt_utils import compressor, estimator

class OptimizedAIService:
    """
    Ultra-efficient AI service with multiple optimization layers:
    1. Local FAQ handler (instant, free, unlimited)
    2. Response caching (avoid repeated API calls)
    3. Multi-provider fallback (Gemini + OpenAI + DeepSeek)
    4. Token-aware prompts (reduce costs)
    5. Rate limiting (maximize free tier usage)
    """
    
    def __init__(self):
        self.provider_manager = provider_manager
        self.cache = response_cache
        self.faq = faq_handler
        self.stats = {
            'local_answers': 0,
            'cache_hits': 0,
            'api_calls': 0,
            'total_queries': 0
        }
    
    def get_answer(self, question: str, subject: str = 'General') -> str:
        """
        Get answer with multi-layer optimization
        """
        self.stats['total_queries'] += 1
        
        # Layer 1: Check local FAQ (instant, free)
        if self.faq.can_answer(question):
            print(f"💡 Local FAQ match!")
            self.stats['local_answers'] += 1
            answer = self.faq.get_answer(question)
            if answer:
                return answer
        
        # Layer 2: Check cache
        metadata = {'subject': subject, 'type': 'qa'}
        cached = self.cache.get(question, metadata)
        if cached:
            print(f"✅ Cache HIT!")
            self.stats['cache_hits'] += 1
            return cached
        
        # Layer 3: Call AI with optimized prompt
        print(f"🔍 Calling AI API...")
        self.stats['api_calls'] += 1
        
        # Create token-efficient prompt
        prompt = compressor.create_efficient_prompt(
            question=question,
            subject=subject
        )
        
        # Estimate tokens
        estimated_tokens = estimator.estimate_tokens(prompt)
        print(f"📊 Estimated tokens: {estimated_tokens}")
        
        # Call with provider fallback
        try:
            response = self.provider_manager.call_with_fallback(
                prompt=prompt,
                temperature=0.7,
                max_tokens=1024
            )
            
            if response:
                # Cache the response
                self.cache.set(question, response, metadata, ttl=3600)
                return response
            else:
                return self._get_fallback_response()
        
        except Exception as e:
            print(f"❌ AI Service Error: {e}")
            return self._get_fallback_response()
    
    def generate_study_plan(self, subject: str, topic: str) -> str:
        """
        Generate study plan with caching
        """
        self.stats['total_queries'] += 1
        
        # Check cache
        cache_key = f"study_plan: {subject} - {topic}"
        metadata = {'subject': subject, 'topic': topic, 'type': 'study_plan'}
        cached = self.cache.get(cache_key, metadata)
        
        if cached:
            print(f"✅ Cache HIT for study plan!")
            self.stats['cache_hits'] += 1
            return cached
        
        # Create compressed prompt
        prompt = compressor.create_study_plan_prompt(subject, topic)
        
        print(f"🔍 Generating study plan...")
        self.stats['api_calls'] += 1
        
        try:
            response = self.provider_manager.call_with_fallback(
                prompt=prompt,
                temperature=0.7,
                max_tokens=1536
            )
            
            if response:
                # Cache for longer (study plans don't change often)
                self.cache.set(cache_key, response, metadata, ttl=7200)
                return response
            else:
                return "⚠️ Couldn't generate study plan. Please try again."
        
        except Exception as e:
            print(f"❌ Study plan error: {e}")
            return f"❌ Error: {str(e)}"
    
    def explain_concept(self, concept: str, level: str = 'intermediate') -> str:
        """
        Explain concept with caching
        """
        self.stats['total_queries'] += 1
        
        # Check cache
        cache_key = f"concept: {concept} ({level})"
        metadata = {'concept': concept, 'level': level, 'type': 'explain'}
        cached = self.cache.get(cache_key, metadata)
        
        if cached:
            print(f"✅ Cache HIT for concept!")
            self.stats['cache_hits'] += 1
            return cached
        
        # Create prompt
        level_desc = {
            'beginner': 'very simple terms for beginners',
            'intermediate': 'clear technical terms',
            'advanced': 'advanced technical detail'
        }
        
        prompt = f"""Explain {concept} in {level_desc.get(level, 'simple terms')}.

Use markdown:
- **Bold** for key terms
- Bullet points for lists
- Real examples
- 1 emoji at end

Keep concise (max 150 words)."""
        
        print(f"🔍 Explaining concept...")
        self.stats['api_calls'] += 1
        
        try:
            response = self.provider_manager.call_with_fallback(
                prompt=prompt,
                temperature=0.7,
                max_tokens=512
            )
            
            if response:
                self.cache.set(cache_key, response, metadata, ttl=3600)
                return response
            else:
                return "⚠️ Couldn't explain concept. Please try again."
        
        except Exception as e:
            print(f"❌ Concept explanation error: {e}")
            return f"❌ Error: {str(e)}"
    
    def _get_fallback_response(self) -> str:
        """Return user-friendly error message"""
        return """⚠️ **Temporary Service Issue**

All AI providers are currently unavailable. This might be due to:
- Rate limits reached (resets every minute)
- Temporary API issues

**What you can do:**
- Wait 60 seconds and try again
- Try a simpler question
- Check your internet connection

Your question will be answered shortly! 🙏"""
    
    def get_stats(self) -> dict:
        """Get service statistics"""
        cache_stats = self.cache.stats()
        provider_stats = self.provider_manager.get_stats()
        faq_stats = self.faq.stats()
        
        # Calculate efficiency
        total = self.stats['total_queries']
        if total > 0:
            free_percentage = ((self.stats['local_answers'] + self.stats['cache_hits']) / total) * 100
        else:
            free_percentage = 0
        
        return {
            'usage': self.stats,
            'efficiency': {
                'free_answers_percentage': round(free_percentage, 1),
                'api_call_percentage': round(100 - free_percentage, 1)
            },
            'cache': cache_stats,
            'providers': provider_stats,
            'faq': faq_stats
        }
    
    def add_faq(self, key: str, answer: str, keywords: list):
        """Add new FAQ to local database"""
        self.faq.add_faq(key, answer, keywords)
    
    def clear_cache(self):
        """Clear expired cache entries"""
        self.cache.clear_expired()
        print("✅ Cache cleaned!")


# Global optimized AI service instance
ai_service = OptimizedAIService()
