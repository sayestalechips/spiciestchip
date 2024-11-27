from typing import List, Dict
import anthropic
import os
import logging
from dotenv import load_dotenv
from src.config.settings import ANTHROPIC_API_KEY, CHIP_PERSONALITY, SYSTEM_PROMPT

# Configure logger
logger = logging.getLogger(__name__)

# Load .env from project root
load_dotenv()

class ClaudeHandler:
    def __init__(self):
        if not ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY must be set in environment variables")
            
        self.client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        self.personality = CHIP_PERSONALITY
        self.system_prompt = SYSTEM_PROMPT
        
    def generate_response(self, query: str, context: Dict, conversation_history: List[Dict], relevant_content: Dict) -> str:
        try:
            conversation_context = self._format_conversation_history(conversation_history)
            formatted_content = self._format_relevant_content(relevant_content)
            
            # Log what we're sending to Claude
            logger.debug("Preparing Claude API call:")
            logger.debug(f"Formatted content length: {len(formatted_content)}")
            logger.debug(f"Conversation history length: {len(conversation_history)}")
            
            system_message = (
                f"{self.system_prompt}\n\n"
                "IMPORTANT RULES:\n"
                "1. You MUST construct your response using ONLY the following content.\n"
                "2. When referencing workshops or experiences, ONLY use examples from the provided transcripts.\n"
                "3. NEVER invent or make up workshop experiences.\n"
                "4. If no relevant transcript examples exist, acknowledge this and stick to documented tools/methods.\n\n"
                f"{formatted_content}\n\n"
                "If the provided content doesn't fully address the query, ask clarifying questions.\n"
                "DO NOT make up or suggest anything not contained in the provided content.\n\n"
            )
            
            if conversation_context:
                system_message += f"Previous conversation:\n{conversation_context}"
            
            # Log final message
            logger.debug(f"Final system message length: {len(system_message)}")
            
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1024,
                temperature=0.7,
                system=system_message,
                messages=[{"role": "user", "content": query}]
            )
            
            return response.content[0].text
            
        except Exception as e:
            logger.error(f"Error calling Claude API: {str(e)}")
            return "I apologize, but I'm having trouble generating a response right now."
    
    def _format_conversation_history(self, history: List[Dict]) -> str:
        """Format conversation history while maintaining personality."""
        formatted = []
        for entry in history[-3:]:  # Keep last 3 interactions for context
            formatted.extend([
                f"User: {entry['query']}",
                f"Chip: {entry['response']}",
                ""
            ])
        return "\n".join(formatted)
    
    def _format_relevant_content(self, content: Dict) -> str:
        formatted = []
        
        # Format tools with complete implementation details
        if content.get('tools'):
            formatted.append("\nTOOL IMPLEMENTATIONS:")
            for tool in content['tools']:
                tool_content = tool.page_content
                tool_meta = tool.metadata
                formatted.extend([
                    f"\nTool: {tool_meta.get('tool_name', '')}",
                    f"\nTool Overview:",
                    f"{tool_content}",
                    f"\nSource: {tool_meta.get('source', '')}"
                ])
        
        # Format transcripts
        if content.get('transcripts'):
            formatted.append("\nREAL WORKSHOP EXAMPLES:")
            for transcript in content['transcripts']:
                formatted.extend([
                    f"\nExample:",
                    f"{transcript.page_content}",
                    f"\nSource: {transcript.metadata.get('source', '')}"
                ])
        
        return "\n".join(formatted)