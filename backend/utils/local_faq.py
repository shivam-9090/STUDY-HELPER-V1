"""
Local FAQ handler - answers common questions without API calls
Ultra-fast, free, unlimited usage
"""
import re
from typing import Optional, Dict, List

class LocalFAQHandler:
    """Handles frequently asked questions locally"""
    
    def __init__(self):
        # Engineering FAQs database
        self.faqs = {
            # Computer Science
            'what is oop': {
                'answer': """**Object-Oriented Programming (OOP)** is a programming paradigm based on the concept of "objects" which contain data and code.

**Key Concepts:**
- **Classes**: Blueprints for creating objects
- **Objects**: Instances of classes
- **Encapsulation**: Bundling data and methods together
- **Inheritance**: Creating new classes from existing ones
- **Polymorphism**: Same interface, different implementations

**Real-world Example:**
Think of a car factory (class) that produces cars (objects). Each car has properties (color, model) and methods (start, stop).

**Benefits:**
- Code reusability
- Easy maintenance
- Better organization
- Mirrors real-world entities 🚗""",
                'keywords': ['oop', 'object oriented', 'encapsulation', 'inheritance', 'polymorphism']
            },
            
            'what is data structure': {
                'answer': """**Data Structures** are specialized formats for organizing, processing, and storing data efficiently.

**Common Data Structures:**
- **Array**: Fixed-size sequential collection
- **Linked List**: Nodes connected by pointers
- **Stack**: LIFO (Last In First Out)
- **Queue**: FIFO (First In First Out)
- **Tree**: Hierarchical structure
- **Graph**: Nodes connected by edges
- **Hash Table**: Key-value pairs for fast lookup

**Why Important?**
- Efficient data access and modification
- Optimal use of memory
- Better algorithm performance
- Foundation for complex systems 📊""",
                'keywords': ['data structure', 'array', 'linked list', 'stack', 'queue', 'tree', 'graph']
            },
            
            'what is algorithm': {
                'answer': """**Algorithm** is a step-by-step procedure to solve a problem or perform a computation.

**Key Properties:**
- **Input**: Zero or more inputs
- **Output**: At least one output
- **Definiteness**: Clear and unambiguous steps
- **Finiteness**: Terminates after finite steps
- **Effectiveness**: Each step must be basic enough to execute

**Example (Finding Maximum):**
1. Start with first number as max
2. Compare each number with max
3. If number > max, update max
4. Return max

**Analysis:**
- **Time Complexity**: How long it takes
- **Space Complexity**: How much memory it uses 🧮""",
                'keywords': ['algorithm', 'time complexity', 'space complexity', 'big o']
            },
            
            # General
            'hello': {
                'answer': "👋 Hello! I'm your AI Study Helper. Ask me anything about engineering subjects and I'll help you learn!",
                'keywords': ['hello', 'hi', 'hey', 'greetings']
            },
            
            'how are you': {
                'answer': "I'm doing great, thanks for asking! 😊 Ready to help you with your studies. What would you like to learn today?",
                'keywords': ['how are you', 'how r u', 'whatsup']
            }
        }
        
        # Build keyword index
        self.keyword_index = self._build_keyword_index()
    
    def _build_keyword_index(self) -> Dict[str, List[str]]:
        """Build index of keywords to FAQ keys"""
        index = {}
        for faq_key, faq_data in self.faqs.items():
            for keyword in faq_data['keywords']:
                if keyword not in index:
                    index[keyword] = []
                index[keyword].append(faq_key)
        return index
    
    def _normalize_query(self, query: str) -> str:
        """Normalize query for matching"""
        return re.sub(r'[^\w\s]', '', query.lower()).strip()
    
    def can_answer(self, query: str) -> bool:
        """Check if this is a FAQ we can answer locally"""
        normalized = self._normalize_query(query)
        
        # Direct match
        if normalized in self.faqs:
            return True
        
        # Keyword match
        for keyword in self.keyword_index:
            if keyword in normalized:
                return True
        
        # Short queries we can handle locally
        if len(normalized.split()) <= 5:
            for faq_key in self.faqs:
                if faq_key in normalized or normalized in faq_key:
                    return True
        
        return False
    
    def get_answer(self, query: str) -> Optional[str]:
        """Get answer from local FAQ database"""
        normalized = self._normalize_query(query)
        
        # Direct match
        if normalized in self.faqs:
            return self.faqs[normalized]['answer']
        
        # Keyword match - find best match
        best_match = None
        max_score = 0
        
        for faq_key, faq_data in self.faqs.items():
            score = 0
            for keyword in faq_data['keywords']:
                if keyword in normalized:
                    score += len(keyword)  # Longer keywords = better match
            
            if score > max_score:
                max_score = score
                best_match = faq_key
        
        if best_match:
            return self.faqs[best_match]['answer']
        
        return None
    
    def add_faq(self, key: str, answer: str, keywords: List[str]):
        """Add new FAQ to database"""
        self.faqs[key] = {
            'answer': answer,
            'keywords': keywords
        }
        # Rebuild index
        self.keyword_index = self._build_keyword_index()
    
    def stats(self) -> Dict:
        """Get FAQ statistics"""
        return {
            'total_faqs': len(self.faqs),
            'total_keywords': len(self.keyword_index),
            'categories': list(set(k.split()[0] for k in self.faqs.keys()))
        }


# Global FAQ handler instance
faq_handler = LocalFAQHandler()
