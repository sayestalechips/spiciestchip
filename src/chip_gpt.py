from typing import Dict, List, Optional
import uuid
import pandas as pd
import os
from dotenv import load_dotenv
from content_processor import ContentProcessor
from claude_handler import ClaudeHandler
import logging
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from config.settings import ANTHROPIC_API_KEY, CHIP_PERSONALITY, SYSTEM_PROMPT
from course_prompts import (
    PERSONALITIES, 
    AF_RANKS, 
    AF_SUBCULTURES, 
    AF_KEY_POSITIONS, 
    AF_INTERACTION_NORMS,
    ICEBREAKER_TOOLS
)
from conversation_manager import ConversationManager

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChipGPT:
    def __init__(self, content_dir: str):
        """Initialize ChipGPT with all components."""
        self.content_dir = content_dir
        
        # Load content first
        self.content = self._load_content()
        
        # Check if vector store exists
        if os.path.exists(os.path.join(content_dir, 'chroma')):
            self.vector_store = Chroma(
                persist_directory=os.path.join(content_dir, 'chroma'),
                embedding_function=OpenAIEmbeddings()
            )
        else:
            # Process content and create vector store
            processor = ContentProcessor()
            self.vector_store = processor.process_content(
                input_dir=os.path.join(os.path.dirname(content_dir), 'raw_courses'),
                output_dir=os.path.join(content_dir, 'chroma')
            )
        
        self.claude = ClaudeHandler()
        self.conversation_manager = ConversationManager()
        
    def process_query(self, 
                     query: str, 
                     session_id: Optional[str] = None) -> str:
        """Process user query with full context awareness."""
        # Ensure we have a session ID
        if not session_id:
            session_id = str(uuid.uuid4())
            
        # Get conversation context
        conversation_history = self.conversation_manager.get_conversation_history(session_id)
        session_context = self.conversation_manager.get_session_context(session_id)
        
        # Analyze query and get relevant content
        intent = self._analyze_intent(query, session_context)
        relevant_content = self._get_relevant_content(query, intent)
        
        # Get response from Claude
        response = self.claude.generate_response(
            query=query,
            context=session_context,
            conversation_history=conversation_history,
            relevant_content=relevant_content
        )
        
        # Update conversation history
        logger.info(f"Adding interaction to history - Query: {query[:50]}...")
        self.conversation_manager.add_interaction(
            session_id=session_id,
            query=query,
            response=response,
            context={'intent': intent, 'content_used': relevant_content}
        )
        logger.info(f"Current history length: {len(conversation_history)}")
        
        return response
    
    def _analyze_intent(self, query: str, session_context: Dict) -> Dict:
        """Analyze query intent with session context."""
        intent = {
            'categories': self._identify_categories(query),
            'needs': self._identify_needs(query, session_context),
            'missing_context': []
        }
        
        # Always check these unless explicitly provided in query
        if not any(word in query.lower() for word in ['help', 'what do you do', 'who are you']):
            if 'objective' not in session_context and not any(word in query.lower() for word in ['for', 'trying to', 'need to']):
                intent['missing_context'].append('What are you trying to achieve?')
            
            if 'group_size' not in session_context and not any(word in query.lower() for word in ['people', 'participants', 'group of']):
                intent['missing_context'].append('How many people are you working with?')
            
            if 'time_available' not in session_context and not any(word in query.lower() for word in ['minutes', 'hours', 'time']):
                intent['missing_context'].append('How much time do you have?')
            
            if 'experience_level' not in session_context and not any(word in query.lower() for word in ['new to', 'experienced', 'beginner']):
                intent['missing_context'].append('What\'s your experience level with facilitation?')
        
        return intent
    
    def _get_relevant_content(self, query: str, intent: Dict) -> Dict:
        """Get relevant content using vector similarity search."""
        docs = self.vector_store.similarity_search(query, k=3)
        
        relevant = {
            'tools': [],
            'transcripts': [],
            'video_links': []
        }
        
        for doc in docs:
            if doc.metadata['type'] == 'tool':
                relevant['tools'].append(doc)
            else:
                relevant['transcripts'].append(doc)
                
        return relevant
    
    def _find_specific_tools(self, query: str) -> List[Dict]:
        """Find specific tools mentioned in query."""
        tools = []
        for _, tool in self.content.iterrows():
            if tool['tool_name'].lower() in query.lower():
                tools.append(tool.to_dict())
        return tools[:3]  # Limit to top 3 most relevant
    
    def _find_tools_by_needs(self, needs: List[str]) -> List[Dict]:
        """Find tools that match identified needs with semantic search."""
        tools = []
        for need in needs:
            results = self.vector_store.similarity_search(
                need,
                k=3,
                filter={"content_type": "tool"}
            )
            tools.extend([doc.metadata for doc in results])
        
        # Deduplicate and rank results
        return self._rank_and_deduplicate_tools(tools)
    
    def _rank_and_deduplicate_tools(self, tools: List[Dict]) -> List[Dict]:
        """Rank tools by relevance score and remove duplicates."""
        seen = set()
        ranked_tools = []
        
        for tool in tools:
            tool_id = tool.get('tool_name', '')
            if tool_id and tool_id not in seen:
                seen.add(tool_id)
                ranked_tools.append(tool)
        
        return ranked_tools[:3]
    
    def _get_facilitation_tips(self, tools: List[Dict]) -> List[str]:
        """Extract facilitation tips for given tools."""
        tips = []
        for tool in tools:
            if 'transcription' in tool and tool['transcription']:
                tips.append(tool['transcription'])
        return tips
    
    def _load_content(self) -> pd.DataFrame:
        """Load and combine all course content from CSVs."""
        all_content = []
        
        # Load all CSV files from the data directory
        for file in os.listdir(self.content_dir):
            if file.endswith('.csv'):
                file_path = os.path.join(self.content_dir, file)
                df = pd.read_csv(file_path)
                # Add source file as a column
                df['source_file'] = file.replace('.csv', '')
                all_content.append(df)
        
        if not all_content:
            raise ValueError(f"No content files found in {self.content_dir}")
        
        combined_content = pd.concat(all_content, ignore_index=True)
        logger.debug(f"Loaded content shape: {combined_content.shape}")
        logger.debug(f"Content columns: {combined_content.columns}")
        return combined_content
    
    def _identify_categories(self, query: str) -> List[str]:
        """Identify query categories."""
        categories = []
        
        # Check for tool-specific queries
        for _, tool in self.content.iterrows():
            if tool['tool_name'].lower() in query.lower():
                categories.append('tool_specific')
                break
        
        # Check for facilitation needs
        facilitation_keywords = ['workshop', 'facilitate', 'run', 'lead', 'guide']
        if any(keyword in query.lower() for keyword in facilitation_keywords):
            categories.append('facilitation')
        
        return categories
    
    def _identify_needs(self, query: str, context: Dict) -> List[str]:
        """Identify user needs from query."""
        needs = []
        
        # Common need patterns
        need_patterns = {
            'creativity': ['creative', 'ideate', 'brainstorm'],
            'decision_making': ['decide', 'choose', 'select', 'prioritize'],
            'team_building': ['team', 'group', 'collaborate'],
            'problem_solving': ['solve', 'problem', 'challenge']
        }
        
        for need, keywords in need_patterns.items():
            if any(keyword in query.lower() for keyword in keywords):
                needs.append(need)
        
        return needs
    
    def _identify_missing_context(self, query: str, context: Dict) -> List[str]:
        """Identify missing context needed for better responses."""
        missing = []
        
        if 'group_size' not in context and 'participants' not in query.lower():
            missing.append('group_size')
        if 'time_available' not in context and 'time' not in query.lower():
            missing.append('time_available')
        
        return missing
    
    def _tool_matches_needs(self, tool: Dict, needs: List[str]) -> bool:
        """Check if tool matches identified needs."""
        tool_text = f"{tool['tool_name']} {tool['description']} {tool['use_cases']}"
        return any(need in tool_text.lower() for need in needs)
    
    def _build_prompt(self, query: str, relevant_content: List[Dict]) -> str:
        """Build prompt with relevant context."""
        context_parts = []
        
        # Add AF context subtly
        af_context = {
            'ranks': AF_RANKS,
            'norms': AF_INTERACTION_NORMS,
            'subcultures': AF_SUBCULTURES
        }
        
        # Add tool-specific content
        for content in relevant_content:
            context_parts.extend([
                f"\nTool: {content['name']}",
                f"Description: {content['description']}",
                f"Best For: {content['use_case']}",
                f"Setup: Works with {content['participants']} and takes {content['time_needed']}",
                f"Reference: {content['url']}\n"
            ])
        
        prompt = f"""Help me respond to this facilitation query: "{query}"

Relevant facilitation knowledge:
{"".join(context_parts)}

AF Context (use subtly):
{str(af_context)}

Remember to:
1. Be conversational and engaging
2. Draw from our specific tools and experience
3. Only mention tools and videos if truly relevant
4. Focus on practical guidance
5. Keep our unique facilitation style
6. Consider AF culture and dynamics naturally

Respond as an experienced facilitator would."""

        return prompt