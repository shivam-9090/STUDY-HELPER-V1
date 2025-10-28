import os
from typing import Optional
import google.generativeai as genai
from datetime import datetime
import time

class AIService:
    """
    AI Service for handling study-related queries using Google Gemini
    with smart fallback and rate limiting
    """
    
    def __init__(self):
        # Load all API keys
        self.api_keys = self._load_api_keys()
        self.current_key_index = 0
        
        # Rate limiting tracking
        self.request_count = {}
        self.last_reset = {}
        self.failed_keys = set()  # Track temporarily failed keys
        
        # Configure initial API key
        if self.api_keys:
            self._configure_api_key(self.api_keys[0])
        else:
            self.model = None
    
    def _load_api_keys(self):
        """Load all available API keys from environment"""
        keys = []
        
        # Primary key
        primary = os.getenv('AI_API_KEY', '')
        if primary:
            keys.append(primary.strip())
        
        # Backup key
        backup = os.getenv('AI_API_KEY_BACKUP', '')
        if backup:
            keys.append(backup.strip())
        
        # Additional backup keys (support up to 10 keys)
        for i in range(2, 10):
            key = os.getenv(f'AI_API_KEY_BACKUP_{i}', '')
            if key:
                keys.append(key.strip())
        
        print(f"✅ Loaded {len(keys)} API key(s) for fallback")
        return keys
    
    def _configure_api_key(self, api_key):
        """Configure Google AI with specific API key"""
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash')
            
            # Initialize rate limiting for this key
            if api_key not in self.request_count:
                self.request_count[api_key] = 0
                self.last_reset[api_key] = datetime.now()
            
            return True
        except Exception as e:
            print(f"⚠️ Failed to configure API key: {e}")
            return False
    
    def _switch_to_next_key(self):
        """Switch to next available API key"""
        if len(self.api_keys) <= 1:
            return False
        
        # Try next keys
        for i in range(1, len(self.api_keys)):
            next_index = (self.current_key_index + i) % len(self.api_keys)
            next_key = self.api_keys[next_index]
            
            # Skip temporarily failed keys
            if next_key in self.failed_keys:
                continue
            
            print(f"🔄 Switching to backup API key #{next_index + 1}")
            if self._configure_api_key(next_key):
                self.current_key_index = next_index
                return True
        
        return False
    
    def _check_rate_limit(self, api_key):
        """Check if approaching rate limits for this key"""
        now = datetime.now()
        
        # Reset counter every minute
        if api_key in self.last_reset:
            if (now - self.last_reset[api_key]).seconds >= 60:
                self.request_count[api_key] = 0
                self.last_reset[api_key] = now
        
        # Free tier: 15 requests per minute - stay under limit
        if self.request_count[api_key] >= 14:
            print(f"⚠️ Rate limit approaching for current key")
            return False
        
        return True
    
    def _make_request_with_fallback(self, request_func):
        """Make API request with automatic fallback to backup keys"""
        max_retries = len(self.api_keys) if self.api_keys else 1
        
        for attempt in range(max_retries):
            try:
                current_key = self.api_keys[self.current_key_index]
                
                # Check rate limit before request
                if not self._check_rate_limit(current_key):
                    if self._switch_to_next_key():
                        continue
                    else:
                        time.sleep(2)  # Brief pause
                
                # Make the request
                result = request_func()
                
                # Success! Track the request
                self.request_count[current_key] = self.request_count.get(current_key, 0) + 1
                
                # Remove from failed keys if recovered
                if current_key in self.failed_keys:
                    self.failed_keys.remove(current_key)
                
                return result
                
            except Exception as e:
                error_str = str(e)
                print(f"❌ API Error (attempt {attempt + 1}/{max_retries}): {error_str}")
                
                # Check if it's a quota/rate limit error
                if "429" in error_str or "quota" in error_str.lower() or "rate" in error_str.lower():
                    current_key = self.api_keys[self.current_key_index]
                    self.failed_keys.add(current_key)
                    
                    # Try next key
                    if not self._switch_to_next_key():
                        if attempt < max_retries - 1:
                            print("⏳ All keys exhausted, waiting 60 seconds...")
                            time.sleep(60)
                            self.failed_keys.clear()
                        else:
                            raise Exception("⚠️ All API keys exceeded quota. Please wait a minute and try again.")
                else:
                    raise e
        
        raise Exception("Failed to get AI response after all retries")
        
    def get_answer(self, question: str, subject: str = 'General') -> str:
        """
        Get answer to a student's question using Gemini AI
        """
        if not self.model:
            return "AI service not configured. Please add your API key to .env file."
        
        def make_request():
            prompt = f"""You are an expert AI tutor helping engineering students learn effectively.

Subject: {subject}
Question: {question}

RESPONSE FORMAT (STRICT):
1. Start with a brief, friendly greeting if appropriate
2. Provide a clear, direct answer
3. Break down complex ideas into simple parts
4. Use proper markdown ONLY for formatting:
   - **Bold** for key terms, formulas, or important concepts
   - *Italic* for definitions or gentle emphasis
   - Use "-" for bullet points in lists
   - Use "1." "2." "3." for numbered steps
   - Use "###" only for major section headers (if needed)
5. NO decorative asterisks, NO unnecessary symbols
6. Write in natural, conversational English
7. Add ONE relevant emoji at the end if it fits naturally

CONTENT GUIDELINES:
- Explain like you're talking to a friend who wants to understand
- Use real-world examples and analogies
- For math problems: show step-by-step solutions with **bold** for answers
- For concepts: define → explain → example
- Keep paragraphs short (2-4 sentences max)
- Use line breaks between different ideas
- Be encouraging but not over-enthusiastic
- If complex, add a "**Key Takeaway:**" section at the end

Provide your answer now:"""
            
            response = self.model.generate_content(
                prompt,
                generation_config={
                    'temperature': 0.7,
                    'top_p': 0.95,
                    'top_k': 40,
                    'max_output_tokens': 1024,
                }
            )
            return response.text
        
        try:
            return self._make_request_with_fallback(make_request)
        except Exception as e:
            error_msg = str(e).lower()
            if "quota" in error_msg or "429" in error_msg or "rate" in error_msg:
                return "⚠️ **All API Keys Exhausted**\n\nAll available API keys have reached their quota limits. Please wait a minute and try again.\n\n**Tips:**\n- Wait 60 seconds for quota to reset\n- Add more backup API keys in .env file\n- Consider upgrading to paid tier for higher limits"
            elif "404" in error_msg:
                return "⚠️ I couldn't connect to the AI service. Please check the API configuration."
            return f"❌ Something went wrong: {str(e)}"

    def generate_study_plan(self, subject: str, topic: str) -> str:
        """
        Generate a study plan for a specific topic using Gemini AI
        """
        if not self.model:
            return "AI service not configured. Please add your API key to .env file."
        
        try:
            prompt = f"""Create a comprehensive 4-week study plan for an engineering student.

Subject: {subject}
Topic: {topic}

FORMAT YOUR PLAN EXACTLY LIKE THIS:

### Week 1: Foundation Building 🌱
**Focus:** Understanding the basics

**What to Learn:**
- [List 3-4 fundamental concepts]

**Practice Tasks:**
- [List 2-3 easy exercises or problems]

**Time:** 5-7 hours this week

---

### Week 2: Intermediate Concepts 📚
**Focus:** Building on fundamentals

**What to Learn:**
- [List 3-4 intermediate topics]

**Practice Tasks:**
- [List 2-3 moderate difficulty problems]

**Time:** 6-8 hours this week

---

### Week 3: Advanced Topics 🚀
**Focus:** Mastering complex ideas

**What to Learn:**
- [List 3-4 advanced concepts]

**Practice Tasks:**
- [List 2-3 challenging problems or mini-projects]

**Time:** 7-9 hours this week

---

### Week 4: Review & Master ✅
**Focus:** Consolidation and testing

**Activities:**
- Complete revision of all topics
- Practice with past papers or real problems
- Identify and strengthen weak areas
- Final self-assessment test

**Time:** 6-8 hours this week

---

**📌 Pro Tips:**
- [Add 2-3 specific study tips for this topic]

**🎯 Success Metrics:**
- [How to know you've mastered this topic]

RULES:
- Use **bold** for labels and emphasis
- Use bullet points with "-"
- Keep each point concise (one line)
- Be specific to the topic
- No unnecessary symbols or decorations

Generate the plan:"""
            
            response = self.model.generate_content(
                prompt,
                generation_config={
                    'temperature': 0.7,
                    'max_output_tokens': 1536,
                }
            )
            return response.text
        except Exception as e:
            error_msg = str(e).lower()
            if "quota" in error_msg or "429" in error_msg or "rate" in error_msg:
                return "⚠️ **API Rate Limit Reached**\n\nPlease wait a moment and try again. Free tier has limited requests per minute."
            return f"❌ Couldn't generate study plan: {str(e)}"

    def explain_concept(self, concept: str, level: str = 'intermediate') -> str:
        """
        Explain a concept at different difficulty levels using Gemini AI
        """
        if not self.model:
            return "AI service not configured. Please add your API key to .env file."
        
        try:
            level_specs = {
                'beginner': {
                    'audience': 'someone with no prior knowledge',
                    'language': 'very simple, everyday words',
                    'depth': 'basic understanding only',
                    'examples': 'real-life analogies and simple examples',
                    'math': 'minimal or no math, focus on intuition'
                },
                'intermediate': {
                    'audience': 'a student who knows the basics',
                    'language': 'clear technical terms with explanations',
                    'depth': 'detailed with some theory',
                    'examples': 'practical engineering examples',
                    'math': 'include formulas and calculations'
                },
                'advanced': {
                    'audience': 'an advanced student or professional',
                    'language': 'precise technical terminology',
                    'depth': 'comprehensive with theoretical foundation',
                    'examples': 'complex applications and edge cases',
                    'math': 'rigorous mathematical treatment'
                }
            }
            
            spec = level_specs.get(level, level_specs['intermediate'])
            
            prompt = f"""Explain this engineering concept clearly and effectively.

**Concept:** {concept}
**Level:** {level} (for {spec['audience']})

STRUCTURE YOUR EXPLANATION:

### What is {concept}?
[2-3 sentence definition in {spec['language']}]

### Core Idea
[Explain the fundamental principle in {spec['depth']}]

### How It Works
[Step-by-step breakdown or mechanism]

### Example
[{spec['examples']}]

{f"### Formula/Math" if level != 'beginner' else ""}
{f"[{spec['math']}]" if level != 'beginner' else ""}

### Real-World Application
[Where and why this is used in engineering]

### Key Points to Remember
- [3-4 bullet points summarizing the essentials]

FORMATTING RULES:
- Use **bold** for the concept name and important terms
- Use *italic* for definitions
- Use "-" for bullet points
- Use "###" for section headers
- Short paragraphs (2-4 sentences)
- Natural, conversational tone
- NO decorative symbols or extra asterisks
- Add ONE emoji at the end if it fits

Explain {concept} now:"""
            
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"❌ Couldn't explain concept: {str(e)}"

    def get_subject_topics(self, subject: str) -> list:
        """Get common topics for a subject"""
        topic_mapping = {
            'Mathematics': ['Calculus', 'Algebra', 'Geometry', 'Statistics', 'Trigonometry'],
            'Physics': ['Mechanics', 'Thermodynamics', 'Electromagnetism', 'Optics', 'Quantum Physics'],
            'Chemistry': ['Organic Chemistry', 'Inorganic Chemistry', 'Physical Chemistry', 'Analytical Chemistry'],
            'Computer Science': ['Data Structures', 'Algorithms', 'Operating Systems', 'Databases', 'Networks'],
            'Electrical Engineering': ['Circuit Theory', 'Digital Electronics', 'Power Systems', 'Control Systems'],
            'Mechanical Engineering': ['Thermodynamics', 'Fluid Mechanics', 'Machine Design', 'Manufacturing'],
            'Civil Engineering': ['Structural Analysis', 'Geotechnical Engineering', 'Transportation', 'Environmental'],
        }
        
        return topic_mapping.get(subject, ['General Topics'])
