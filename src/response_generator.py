class ResponseGenerator:
    def __init__(self):
        self.facilitation_phrases = {
            'suggestions': [
                "Based on your situation, I'd recommend",
                "Given what you've described, here's what I suggest",
                "In my experience, this would be perfect for your needs"
            ],
            'clarifications': [
                "To help you better, I need to know",
                "Could you tell me more about",
                "It would help if I understood"
            ],
            'transitions': [
                "Let me explain why this works well",
                "Here's how this helps",
                "This is particularly effective because"
            ]
        }
        
    def generate_facilitation_guidance(self, content: list, intent: dict) -> str:
        """Generate facilitation-focused guidance."""
        response = []
        
        # Start with understanding
        response.append(self._select_phrase('suggestions'))
        
        # Add tool recommendation
        for tool in content[:2]:  # Limit to top 2 most relevant tools
            response.append(self._format_tool_suggestion(tool))
            
        # Add facilitation tips
        if 'facilitation_tips' in content[0]:
            tips = self._extract_tips(content[0]['facilitation_tips'])
            if tips:
                response.append("\nKey facilitation tips:")
                response.extend([f"- {tip}" for tip in tips])
                
        return "\n".join(response)
        
    def generate_recommendation_response(self, content: list, intent: dict) -> str:
        """Generate tool recommendation response."""
        response = []
        
        # Acknowledge needs
        if 'needs' in intent:
            response.append(self._acknowledge_needs(intent['needs']))
            
        # Present recommendations
        response.append(self._select_phrase('suggestions'))
        for tool in content[:2]:
            response.append(self._format_tool_recommendation(tool))
            
        # Add contextual guidance
        response.append(self._add_contextual_guidance(intent))
        
        # Add follow-up
        response.append("\nWould you like me to explain any of these tools in more detail?")
        
        return "\n".join(response)
        
    def _format_tool_suggestion(self, tool: dict) -> str:
        """Format a tool suggestion with key details."""
        return f"""
{tool['Name']} - {tool['Complexity']} complexity
• {tool['Description']}
• Best for: {tool['Number of Participants']}
• Takes: {tool['Length of Time']}
"""
        
    def _extract_tips(self, tips_json: str) -> list:
        """Extract and format facilitation tips."""
        try:
            tips = json.loads(tips_json)
            return [tip.strip() for tip in tips if tip.strip()]
        except:
            return []
            
    def _acknowledge_needs(self, needs: list) -> str:
        """Generate acknowledgment of user needs."""
        if 'time_sensitive' in needs:
            return "I understand you need something quick and effective."
        elif 'prefer_simple' in needs:
            return "I'll focus on straightforward, easy-to-implement solutions."
        return "Here's what I think would work well for your situation."
        
    def _select_phrase(self, category: str) -> str:
        """Select appropriate phrase for response."""
        return np.random.choice(self.facilitation_phrases[category])
        
    def _add_contextual_guidance(self, intent: dict) -> str:
        """Add context-specific guidance."""
        guidance = []
        
        if 'group_size_important' in intent.get('needs', []):
            guidance.append("\nNote: These tools work best with the group sizes indicated above.")
            
        if 'time_sensitive' in intent.get('needs', []):
            guidance.append("\nI've focused on tools that can be implemented quickly while still being effective.")
            
        return "\n".join(guidance)