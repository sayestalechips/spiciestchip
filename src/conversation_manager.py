from typing import List, Dict, Optional
from datetime import datetime
import json

class ConversationManager:
    def __init__(self):
        self.conversations: Dict[str, List[Dict]] = {}
        self.session_metadata: Dict[str, Dict] = {}
        
    def start_conversation(self, session_id: str, metadata: Optional[Dict] = None) -> None:
        """Start a new conversation session."""
        self.conversations[session_id] = []
        self.session_metadata[session_id] = {
            'started_at': datetime.now().isoformat(),
            'interaction_count': 0,
            'tools_discussed': set(),
            'identified_needs': set(),
            **(metadata or {})
        }
        
    def add_interaction(self, 
                       session_id: str, 
                       query: str, 
                       response: str, 
                       context: Dict) -> None:
        """Add an interaction to the conversation history."""
        if session_id not in self.conversations:
            self.start_conversation(session_id)
            
        interaction = {
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'response': response,
            'context': context,
        }
        
        self.conversations[session_id].append(interaction)
        self._update_session_metadata(session_id, interaction)
        
    def get_conversation_history(self, 
                               session_id: str, 
                               limit: Optional[int] = None) -> List[Dict]:
        """Get conversation history for a session."""
        history = self.conversations.get(session_id, [])
        if limit:
            return history[-limit:]
        return history
        
    def get_session_context(self, session_id: str) -> Dict:
        """Get accumulated context for a session."""
        return {
            'metadata': self.session_metadata.get(session_id, {}),
            'history_length': len(self.conversations.get(session_id, [])),
            'identified_needs': list(self.session_metadata.get(session_id, {}).get('identified_needs', set())),
            'tools_discussed': list(self.session_metadata.get(session_id, {}).get('tools_discussed', set()))
        }
        
    def _update_session_metadata(self, session_id: str, interaction: Dict) -> None:
        """Update session metadata based on new interaction."""
        metadata = self.session_metadata[session_id]
        metadata['interaction_count'] += 1
        
        # Update tools discussed
        if 'tool_mention' in interaction.get('context', {}):
            metadata['tools_discussed'].add(interaction['context']['tool_mention'])
            
        # Update identified needs
        if 'needs' in interaction.get('context', {}):
            metadata['identified_needs'].update(interaction['context']['needs'])
            
        # Update last interaction time
        metadata['last_interaction'] = interaction['timestamp']