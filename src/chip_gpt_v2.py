from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
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
        # Initialize vector store
        if os.path.exists(os.path.join(content_dir, 'chroma')):
            self.vector_store = Chroma(
                persist_directory=os.path.join(content_dir, 'chroma'),
                embedding_function=OpenAIEmbeddings()
            )
        else:
            processor = ContentProcessor()
            self.vector_store = processor.process_content(
                data_dir=os.path.join(os.path.dirname(content_dir), 'raw_courses')
            )
        self.client = Anthropic()
        self.context_window = 5
        self.base_prompt = """You are Chip, an expert facilitator who creates inclusive, engaging workshop environments.

Core Identity:
- Expert in creating psychological safety
- Deep knowledge of group dynamics and facilitation techniques
- Focus on human connection and authentic participation
- Understanding of organizational dynamics without overemphasizing hierarchy

Communication Approach:
1. Create an environment where everyone feels valued as individuals
2. Be warm and conversational while maintaining professionalism
3. Provide practical, actionable guidance
4. Include relevant examples that focus on human dynamics
5. Only reference organizational structure when directly relevant to the challenge

Remember: While you understand military culture, your primary focus is on creating spaces where people can connect as individuals first."""

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
For tools and activities:
1. Acknowledge the specific situation/need
2. Reference relevant tools or techniques from our content
3. Provide specific strategies that encourage equal participation
4. Include concrete examples focused on human connection
5. Always reference video links when available
6. Consider group dynamics while maintaining individual focus

Remember: Create spaces where people can authentically connect. If clarification is needed, ask before proceeding."""

        return prompt
    
    def process_query(self, query: str) -> str:
        try:
            # Get relevant context from vector store
            relevant_docs = self.vector_store.similarity_search(
                query,
                k=3,
                filter={"content_type": "tool"}
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
        
        # Check for personality-related keywords
        if any(word in query for word in ['personality', 'dtip', 'difficult person', 'bossy', 'quiet']):
            return 'personality'
        
        # Check for tool-related keywords
        if any(word in query for word in ['tool', 'exercise', 'activity', 'icebreaker', 'brainstorm']):
            return 'tool'
        
        return 'general'