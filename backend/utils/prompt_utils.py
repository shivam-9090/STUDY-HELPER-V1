"""
Prompt compression and token optimization utilities
"""
import re
from typing import Dict, List

class PromptCompressor:
    """Compress prompts to reduce token usage"""
    
    @staticmethod
    def compress_whitespace(text: str) -> str:
        """Remove extra whitespace"""
        # Replace multiple spaces with single space
        text = re.sub(r' +', ' ', text)
        # Replace multiple newlines with max 2
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()
    
    @staticmethod
    def remove_redundant_instructions(text: str) -> str:
        """Remove common redundant phrases"""
        redundant = [
            'please note that',
            'it is important to',
            'you should know that',
            'as you can see',
            'in other words',
            'basically',
            'essentially'
        ]
        for phrase in redundant:
            text = re.sub(phrase, '', text, flags=re.IGNORECASE)
        return text
    
    @staticmethod
    def create_efficient_prompt(
        question: str,
        subject: str = None,
        context: List[str] = None,
        max_context_items: int = 3
    ) -> str:
        """Create token-efficient prompt"""
        
        # Compact system instruction
        system = "Expert AI tutor. Answer clearly using markdown."
        
        # Add subject if provided
        if subject:
            system += f" Subject: {subject}."
        
        # Add limited context
        context_str = ""
        if context:
            limited_context = context[:max_context_items]
            context_str = "\nContext: " + "; ".join(limited_context)
        
        # Combine
        prompt = f"{system}\n\nQ: {question}{context_str}\n\nA:"
        
        return PromptCompressor.compress_whitespace(prompt)
    
    @staticmethod
    def create_study_plan_prompt(subject: str, topic: str) -> str:
        """Compact study plan prompt"""
        return f"""Create 4-week study plan.

Subject: {subject}
Topic: {topic}

Format:
### Week 1: Foundation
- What: [3-4 basics]
- Tasks: [2-3 exercises]
- Time: 5-7h

### Week 2: Intermediate
- What: [3-4 topics]
- Tasks: [2-3 problems]
- Time: 6-8h

### Week 3: Advanced
- What: [3-4 concepts]
- Tasks: [2-3 projects]
- Time: 7-9h

### Week 4: Review
- Revision, practice, test
- Time: 6-8h

Add tips and metrics."""


class TokenEstimator:
    """Estimate token count for prompts"""
    
    @staticmethod
    def estimate_tokens(text: str) -> int:
        """Rough token estimation (1 token ≈ 4 characters for English)"""
        # More accurate: count words and punctuation
        words = len(text.split())
        chars = len(text)
        # Average between word-based and char-based estimates
        word_estimate = int(words * 1.3)  # ~1.3 tokens per word
        char_estimate = int(chars / 4)     # ~4 chars per token
        return (word_estimate + char_estimate) // 2
    
    @staticmethod
    def should_compress(text: str, threshold: int = 500) -> bool:
        """Check if text should be compressed"""
        return TokenEstimator.estimate_tokens(text) > threshold
    
    @staticmethod
    def get_token_budget(response_tokens: int = 1024) -> Dict[str, int]:
        """Calculate token budget for request"""
        # Most models have ~4K context limit
        total_context = 4000
        system_prompt = 100
        response_space = response_tokens
        
        available = total_context - system_prompt - response_space
        
        return {
            'total_context': total_context,
            'system_prompt': system_prompt,
            'response_tokens': response_space,
            'available_for_user': available,
            'recommended_max': int(available * 0.8)  # Leave 20% buffer
        }


class ContextSummarizer:
    """Summarize chat context to save tokens"""
    
    @staticmethod
    def summarize_chat_history(messages: List[Dict], max_messages: int = 5) -> List[Dict]:
        """Keep only recent messages to reduce tokens"""
        if len(messages) <= max_messages:
            return messages
        
        # Keep first message (usually important context) and recent messages
        important_first = messages[0]
        recent = messages[-(max_messages-1):]
        
        return [important_first] + recent
    
    @staticmethod
    def extract_key_points(text: str, max_points: int = 3) -> List[str]:
        """Extract key points from long text"""
        # Split into sentences
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        
        # Score sentences by length and position
        scored = []
        for i, sent in enumerate(sentences):
            # Prefer earlier sentences and medium length
            position_score = 1.0 / (i + 1)
            length_score = min(len(sent.split()), 20) / 20
            score = position_score * 0.7 + length_score * 0.3
            scored.append((score, sent))
        
        # Return top N
        scored.sort(reverse=True)
        return [sent for _, sent in scored[:max_points]]


# Global instances
compressor = PromptCompressor()
estimator = TokenEstimator()
summarizer = ContextSummarizer()
