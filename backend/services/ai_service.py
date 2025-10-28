import os
from typing import Optional
import google.generativeai as genai

class AIService:
    """
    AI Service for handling study-related queries using Google Gemini
    """
    
    def __init__(self):
        self.api_key = os.getenv('AI_API_KEY', '')
        if self.api_key:
            genai.configure(api_key=self.api_key)
            # Use gemini-2.5-flash - stable, fast, and lightweight
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        else:
            self.model = None
        
    def get_answer(self, question: str, subject: str = 'General') -> str:
        """
        Get answer to a student's question using Gemini AI
        """
        if not self.model:
            return "AI service not configured. Please add your API key to .env file."
        
        try:
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
            
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            error_msg = str(e)
            if "404" in error_msg:
                return "⚠️ I couldn't connect to the AI service. Please check the API configuration."
            return f"❌ Something went wrong: {error_msg}"

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
            
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
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
