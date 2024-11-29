from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from conversation_manager import ConversationManager
from content_processor_v2 import ContentProcessor
from typing import Dict, List, Optional
import os
from anthropic import Anthropic
import json
import logging
from course_prompts import (
    PERSONALITIES, 
    AF_RANKS, 
    AF_SUBCULTURES, 
    AF_KEY_POSITIONS, 
    AF_INTERACTION_NORMS,
    ICEBREAKER_TOOLS,
    BRAINSTORMING_TOOLS
)

logger = logging.getLogger(__name__)

class ChipGPT:
    def __init__(self, content_dir: str):
        # Initialize vector store with simpler configuration
        if os.path.exists(os.path.join(content_dir, 'chroma')):
            embeddings = OpenAIEmbeddings()
            self.vector_store = Chroma(
                persist_directory=os.path.join(content_dir, 'chroma'),
                embedding_function=embeddings
            )
        else:
            processor = ContentProcessor()
            self.vector_store = processor.process_content(
                data_dir=os.path.join(os.path.dirname(content_dir), 'raw_courses')
            )
        self.client = Anthropic()
        self.context_window = 5
        self.base_prompt = """You are Chip, channeling the exact style and methodology of Stale Chips. 

Core Identity:
- We make spaces where everyone is confident and comfortable enough to be themselves
- Engagement equals better information. Better information yields better results
- Being a real human gets us further faster
- Use casual, direct language like Johnny and John

Here are examples of how to respond to different types of questions:

1. CONCEPT QUESTION EXAMPLE
Q: "What is design thinking?"
A: "Hey there! *adjusts facilitator hat* Design thinking is all about solving problems by focusing on the human experience first. In our Dangerous Facilitation course (Module 3), we break it down into five key steps: Empathize, Define, Ideate, Prototype, and Test. 

Here's a quick video where Johnny walks through it (and yes, you can watch at 2x speed - he almost sounds normal that way! 😉): [video_link]

The coolest part? When you combine this with our core principle that engagement equals better information, you get some seriously powerful results."

2. TOOL REQUEST EXAMPLE
Q: "I need an icebreaker for a new team"
A: "Perfect timing! *pulls out Stale Chips toolbox* From our Dangerous Facilitation toolkit, I'd recommend the 5-Second Test. It's quick, gets everyone involved, and most importantly - creates that psychological safety we're always talking about.

Here's how it works:
[specific steps from our actual content]

We use this one all the time in our workshops because it proves our point that being a real human gets us further faster. Check out this video where John demonstrates it: [video_link]"

3. WHEN WE DON'T HAVE CONTENT EXAMPLE
Q: "How do I handle a difficult stakeholder?"
A: "You know what? We don't have specific Stale Chips content about stakeholder management yet. But here's what I can tell you based on our core principles: engagement equals better information. The more we can get them involved early and authentically, the better our results will be. 

If you're looking for tested techniques though, our Dangerous Facilitation course has some great tools for building trust in any group setting."

Remember:
- Always cite specific Stale Chips content when available
- Reference relevant videos with a touch of humor about speed
- Keep it real and practical
- Never make up content - if we don't have it, say so
- Stay focused on the current question

When sharing tools or techniques, always include:
1. Which course/module it's from
2. Why it works (tied to our principles)
3. Specific steps (from our content)
4. Link to relevant video content"""

        # Dictionary to hold course-specific prompts
        self.course_prompts = {
            'icebreakers': ICEBREAKER_TOOLS,
            'personalities': PERSONALITIES,
            'ranks': AF_RANKS,
            'subcultures': AF_SUBCULTURES,
            'positions': AF_KEY_POSITIONS,
            'norms': AF_INTERACTION_NORMS,
            'brainstorming': BRAINSTORMING_TOOLS
        }
    
    def get_context_specific_prompt(self, query: str, relevant_docs: List) -> str:
        """Build comprehensive prompt combining vector search results and course prompts"""
        context_data = {
            'vector_results': [],
            'course_content': {}
        }
        
        # Process vector search results
        for doc in relevant_docs:
            metadata = doc.metadata
            if metadata.get('content_type') == 'personality':
                context_data['vector_results'].append({
                    'type': 'personality',
                    'name': metadata.get('name'),
                    'characteristics': metadata.get('characteristics'),
                    'strategies': metadata.get('strategies'),
                    'url': metadata.get('url')
                })
            elif metadata.get('content_type') == 'tool':
                context_data['vector_results'].append({
                    'type': 'tool',
                    'name': metadata.get('name'),
                    'description': metadata.get('description'),
                    'use_case': metadata.get('use_case'),
                    'url': metadata.get('url')
                })
        
        # Add relevant course prompts based on query type
        if any(term in query.lower() for term in ['personality', 'difficult', 'manage']):
            context_data['course_content']['personalities'] = self.course_prompts['personalities']
            context_data['course_content']['norms'] = self.course_prompts['norms']
        
        if any(term in query.lower() for term in ['icebreaker', 'start', 'begin']):
            context_data['course_content']['icebreakers'] = self.course_prompts['icebreakers']
        
        if any(term in query.lower() for term in ['brainstorm', 'ideate', 'generate']):
            context_data['course_content']['brainstorming'] = self.course_prompts['brainstorming']
        
        # Always include AF context
        context_data['course_content']['ranks'] = self.course_prompts['ranks']
        context_data['course_content']['subcultures'] = self.course_prompts['subcultures']
        
        # Build the final prompt with example formatting
        prompt = f"""{self.base_prompt}

RELEVANT CONTENT FROM OUR KNOWLEDGE BASE:
{json.dumps(context_data['vector_results'], indent=2)}

COURSE-SPECIFIC GUIDANCE:
{json.dumps(context_data['course_content'], indent=2)}

RESPONSE STRUCTURE:
For tools, always use this exact format:
Tool: [Tool Name]

Tool Overview
- Brief explanation of why this tool fits the situation
- List 4-5 key benefits for the specific context

Step by Step Guide
1. Setup (with timing)
2. Implementation steps (with timing)
3. Wrap-up (with timing)

Link to Video Training
[Include relevant URL]

For personalities, always use this exact format:
Personality: [Personality Type Name]

Personality Overview
- Detailed description of behavioral patterns
- Impact on group dynamics

Tips for Managing the Personality
1. Pre-session strategies
2. During-session techniques
3. Follow-up approaches
4. Specific phrases to use

Link to Video Training
[Include relevant URL]

Remember: Create spaces where people can authentically connect. If clarification is needed, ask before proceeding."""

        return prompt
    
    def process_query(self, query: str) -> str:
        try:
            # Simplified search query
            search_query = f"""
            Find Stale Chips content related to: {query}
            Consider:
            - Specific tools and techniques
            - Course module references
            - Real workshop examples
            - Facilitation principles
            """
            
            # Most basic similarity search - just return k results
            relevant_docs = self.vector_store.similarity_search(
                search_query,
                k=5
            )
            
            # Build comprehensive prompt with both vector results and course content
            system_prompt = self.get_context_specific_prompt(query, relevant_docs)
            
            # Create the response
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1024,
                system=system_prompt,
                messages=[{
                    "role": "user", 
                    "content": f"User question: {query}"
                }]
            )
            
            return response.content
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return f"Sorry, I encountered an error: {str(e)}"

    def _determine_query_type(self, query: str) -> str:
        query = query.lower()
        
        if "what is" in query or "define" in query or "explain" in query:
            return "definition"
        elif "tool" in query or "technique" in query or "activity" in query:
            return "tool"
        elif "personality" in query or "person" in query or "manage" in query:
            return "personality"
        else:
            return "general"