class ConversationContextManager:
    def __init__(self):
        self.current_context = {
            'user_needs': set(),
            'discussed_tools': [],
            'facilitation_style': None,
            'group_context': None,
            'time_constraints': None
        }
        self.conversation_history = []
        
    def update_context(self, query: str, response: str, intent: dict):
        """Update context based on interaction."""
        # Track needs mentioned
        if 'needs' in intent:
            self.current_context['user_needs'].update(intent['needs'])
            
        # Track tools discussed
        if 'tool_specific' in intent.get('categories', []):
            tool_name = self._extract_tool_name(response)
            if tool_name:
                self.current_context['discussed_tools'].append(tool_name)
                
        # Track conversation
        self.conversation_history.append({
            'query': query,
            'response': response,
            'intent': intent,
            'timestamp': datetime.now().isoformat()
        })
        
    def get_context_insights(self) -> dict:
        """Get insights from accumulated context."""
        return {
            'known_needs': list(self.current_context['user_needs']),
            'previous_tools': self.current_context['discussed_tools'],
            'conversation_length': len(self.conversation_history)
        }
        
    def missing_critical_context(self) -> bool:
        """Check if we're missing critical context."""
        if self.conversation_history:
            latest = self.conversation_history[-1]
            # If first interaction and no clear needs identified
            if len(self.conversation_history) == 1 and not self.current_context['user_needs']:
                return True
            # If discussing tools but no group size info
            if 'tool_specific' in latest['intent'].get('categories', []) and not self.current_context['group_context']:
                return True
        return False
        
    def _extract_tool_name(self, response: str) -> str:
        """Extract tool name from response."""
        if "Let me tell you about" in response:
            return response.split("Let me tell you about")[1].split(".")[0].strip()
        return None