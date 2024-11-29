from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from conversation_manager import ConversationManager
from content_processor_v2 import ContentProcessor
from typing import Dict, List, Optional, Tuple
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
import re

logger = logging.getLogger(__name__)

COMMON_SCENARIOS = {
    'shy_sme': {
        'indicators': ['quiet expert', 'technical lead', 'subject matter expert'],
        'approach': [
            'Build psychological safety first',
            'Use written ideation before verbal',
            'Leverage their expertise indirectly',
            'Create structured sharing opportunities'
        ]
    },
    'dominant_senior': {
        'indicators': ['senior leader', 'commander', 'chief'],
        'approach': [
            'Acknowledge experience respectfully',
            'Channel energy to specific tasks',
            'Use structured turn-taking',
            'Create equal participation rules'
        ]
    },
    'resistant_group': {
        'indicators': ['mandatory training', 'forced attendance', 'required workshop'],
        'approach': [
            'Start with their frustrations',
            'Show immediate practical value',
            'Use humor to break tension',
            'Build quick wins early'
        ]
    }
}

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

CONTEXT GATHERING GUIDELINES:
1. Ask ONE clarifying question when critical context is missing. Example:
   User: "I need an icebreaker."
   Response: "Quick question before I jump in - are we talking about a new team or an existing one? That'll help me pick the perfect tool! 🎯"

2. When you have enough context to provide a solid answer, don't ask questions. Example:
   User: "I need an icebreaker for my new team of 12 engineers."
   Response: "Perfect! *pulls out favorite new-team tool* Let me introduce you to..."

3. If you're 70%+ confident about the need but could use minor clarification, provide the answer AND mention the assumption. Example:
   "Based on what you've shared, I'm going to recommend our 5-Second Test (assuming this is an in-person session - but it works virtual too!)..."

RESPONSE EXAMPLES:

1. TOOL RECOMMENDATION (Perfect Context)
User: "I need an icebreaker for my new team of 8 engineers who are working remotely."
Response: "Oh, perfect timing! *virtual facilitator hat = ON* 🎩

The 'Desert Island Tech' icebreaker from our Virtual Facilitation course is exactly what you need here. Engineers typically love this one because it combines tech AND creative thinking.

Quick Setup:
1. Share screen with a simple slide: 'You're stranded on a desert island. You can only bring 3 pieces of technology. What do you pick and why?'
2. Give everyone 30 seconds to think
3. Go round-robin, 1 minute each
4. Pro-tip: You go first to model the vulnerability we're looking for!

Why this works:
- Gets engineers talking about their comfort zone (tech) while being creative
- Creates instant debates about practical vs fun choices
- Shows personality through their choices
- Takes exactly 10 minutes for your group of 8

📺 Check out Johnny demoing this at 14:32 in Module 2 of Virtual Facilitation (and yes, you can watch at 2x speed 😉)"

2. CONCEPT EXPLANATION (Needs Clarification)
User: "How do I handle resistance?"
Response: "Before I dive into our resistance-busting tools, could you share what type of resistance you're seeing? Is it more of a 'arms crossed, not participating' situation, or more of a 'actively challenging everything' vibe? That'll help me point you to the exact right strategy! 🎯"

3. PERSONALITY MANAGEMENT (Partial Context)
User: "There's someone in my workshop who keeps dominating the conversation"
Response: "Ah, the Enthusiastic Expert! (That's what we call them in our Dangerous Facilitation course 😉)

Here's your quick action plan from Module 4:

1. First, remember: their enthusiasm is actually a good thing - we just need to redirect it!

2. Try this exact phrase: 'Thanks for that insight! I'd love to hear how others might build on that idea...'
(Johnny uses this one all the time - check out the demo at 23:45 in the Difficult Personalities video)

3. Give them a specific role: 'Could you help capture the key points on our virtual whiteboard?'

The magic here is that we're not shutting them down - we're channeling their energy into something productive. That's pure Stale Chips methodology right there! 

Want more strategies specifically for this? There's a whole section in Module 4 that breaks down different types of dominant personalities and how to handle each one."

4. WHEN WE DON'T HAVE CONTENT
User: "How do I handle budget discussions?"
Response: "You know what? I'll be straight with you - we don't have specific Stale Chips content about budget facilitation yet. I could make something up, but that wouldn't be very 'real human gets us further faster' of me! 😅

What I CAN share is how we handle potentially tense discussions in our Dangerous Facilitation course. Would you like me to walk you through those techniques? They're designed for any high-stakes conversation."

Remember:
- Always cite specific Stale Chips content when available
- Use casual, direct language with a touch of humor
- Include relevant video timestamps
- If we don't have specific content, we say so
- Keep responses focused and actionable
- Use emojis sparingly but strategically 😉
- Reference Johnny and John's teaching style and examples

When sharing tools or techniques, always include:
1. Which course/module it's from
2. Why it works (tied to our principles)
3. Specific steps (from our content)
4. Relevant video timestamps
5. A touch of Stale Chips personality

CRITICAL CONTENT RULES:
1. NEVER CREATE OR MODIFY CONTENT
   - Do not invent tools, personalities, or lessons
   - Do not modify existing content or techniques
   - Do not make up video timestamps or URLs
   - If you're not 100% certain about content details, say so

2. ALWAYS USE AUTHENTIC SOURCES
   - Only reference tools and content that exist in our knowledge base
   - Use complete, exact URLs from our data sources
   - Include specific video timestamps only if they're in our data
   - Quote exact phrases and definitions from our courses

3. VIDEO REFERENCES ARE REQUIRED
   - Every tool recommendation must include a relevant video link
   - Every personality type must link to its training video
   - Every concept explanation needs a video reference
   - If no video exists for the topic, explicitly state this

4. WHEN IN DOUBT
   - Say "We don't have specific content about that yet"
   - Redirect to related content we do have
   - Be transparent about what you do and don't know
   - Never guess or approximate content details

Example of correct content handling:
✅ "Let me share our 'Desert Island Tech' icebreaker from the Virtual Facilitation course. You can see Johnny demonstrate this at https://stale-chips.com/courses/virtual-facilitation/module-2#timestamp=14:32"

Example of incorrect content handling:
❌ "Here's a great icebreaker I think would work..." [Making up a new tool]
❌ "Check out the video somewhere in Module 2" [Vague reference]
❌ "I believe Johnny might have mentioned..." [Uncertain attribution]

Remember: Our credibility comes from our real, tested content. If we don't have something, we say so!"""

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
        
        # Add confidence thresholds
        self.CONFIDENCE_THRESHOLD = 0.7
        self.MAX_CONTEXT_ITEMS = 3
        
        # Add response templates
        self.response_templates = {
            'tool': {
                'structure': [
                    "🛠️ {tool_name}",
                    "\nWhy This Tool:",
                    "- {context_specific_reason}",
                    "- Perfect for: {use_case}",
                    "\nQuick Setup:",
                    "{setup_steps}",
                    "\nVideo Reference:",
                    "{video_url}"
                ],
                'required_fields': ['tool_name', 'use_case', 'setup_steps', 'video_url']
            },
            'concept': {
                'structure': [
                    "💡 {concept_name}",
                    "\nStale Chips Definition:",
                    "{official_definition}",
                    "\nReal-World Application:",
                    "{practical_example}",
                    "\n📺 Deep dive here: {video_url}"
                ],
                'required_fields': ['concept_name', 'official_definition', 'video_url']
            }
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
            logger.info("Starting query processing...")
            
            # 1. Classify query and identify specific tools
            query_type, confidence = self._classify_query(query)
            logger.info(f"Query classified as: {query_type} with confidence: {confidence}")
            
            # 2. Initialize context data with all required keys
            context_data = {
                'specific_tool': None,
                'general_tips': [],
                'related_content': [],
                'videos': [],
                'content': [],
                'sources': set()
            }
            
            # 3. Get general facilitation guidance from Dangerous course
            dangerous_results = self.vector_store.similarity_search(
                "facilitation tips workshop guidance best practices",
                k=2,
                filter={"source": "Dangerous Course - Sheet1.csv"}
            )
            
            # Process Dangerous course results
            for doc in dangerous_results:
                context_data['general_tips'].append(doc.page_content)
                if 'url' in doc.metadata:
                    context_data['sources'].add(doc.metadata['url'])
            
            logger.info(f"Added {len(dangerous_results)} items from Dangerous course")
            
            # 4. Get tool-specific content if applicable
            if query_type in self.course_prompts:
                for name, details in self.course_prompts[query_type].items():
                    context_data['content'].append({
                        'name': name,
                        'details': details,
                        'type': query_type
                    })
                    if 'url' in details:
                        context_data['sources'].add(details['url'])
            
            # 5. Build prompt with all gathered content
            system_prompt = f"""{self.base_prompt}

RESPONSE FORMAT:
1. For Tools:
   [Tool Name]
   
   What It Is:
   - Brief description
   - Group size and timing
   
   Setup Steps:
   1. Step one
   2. Step two
   etc.
   
   Why It Works:
   - Benefit points
   
   Video Reference:
   [Only include if URL exists in provided content]

2. For Personalities (DTIP Course):
   [Personality Type from DTIP]
   
   Characteristics:
   - List from course content
   
   Management Strategies:
   1. Strategy one
   2. Strategy two
   etc.
   
   Course Reference:
   [DTIP course URL if available]

CONTENT FOR RESPONSE:
{json.dumps(context_data['content'], indent=2)}

Remember:
1. Only reference DTIP for personality management
2. Never create or modify personality types
3. Only include video links that exist in provided content
4. NEVER include timestamps - we don't have these in our content
5. Keep the casual Stale Chips style while maintaining accuracy
6. If you're not sure about specific details, be transparent about it"""

            logger.info("System prompt built. First 100 chars:")
            logger.info(system_prompt[:100])
            
            # 6. Get response from Claude
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1024,
                system=system_prompt,
                messages=[{"role": "user", "content": query}]
            )
            
            return response.content

        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return f"Sorry, I encountered an error: {str(e)}"

    def _extract_key_terms(self, query: str) -> List[str]:
        """Extract meaningful terms from query using regex and stopword removal"""
        # Add implementation
        pass

    def _merge_and_rank_results(
        self, 
        vector_results: List[Dict], 
        structured_results: List[Dict],
        intent_scores: Dict[str, float]
    ) -> List[Dict]:
        """Merge and rank results based on relevance and confidence"""
        all_results = []
        
        # Score and rank each result
        for result in vector_results + structured_results:
            relevance_score = self._calculate_relevance_score(result, intent_scores)
            all_results.append({
                'content': result,
                'score': relevance_score
            })
        
        # Sort by score and return top results
        ranked_results = sorted(all_results, key=lambda x: x['score'], reverse=True)
        return [r['content'] for r in ranked_results[:self.MAX_CONTEXT_ITEMS]]

    def _calculate_relevance_score(
        self, 
        result: Dict, 
        intent_scores: Dict[str, float]
    ) -> float:
        """Calculate relevance score based on multiple factors"""
        score = 0.0
        
        # Factor 1: Match with primary intent
        if result.get('type') in intent_scores:
            score += intent_scores[result['type']] * 0.4
            
        # Factor 2: Content freshness
        if 'timestamp' in result:
            age_penalty = self._calculate_age_penalty(result['timestamp'])
            score += age_penalty * 0.2
            
        # Factor 3: Usage statistics (if available)
        if 'usage_count' in result:
            usage_boost = min(result['usage_count'] / 100, 1.0) * 0.2
            score += usage_boost
            
        # Factor 4: Content completeness
        completeness = self._check_content_completeness(result)
        score += completeness * 0.2
        
        return score

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

    def _classify_query(self, query: str) -> Tuple[str, float]:
        """Enhanced query classification with better personality detection"""
        query_lower = query.lower()
        
        # First check for exact tool/personality names
        for content_type, content_dict in self.course_prompts.items():
            for name in content_dict.keys():
                if name.lower() in query_lower:
                    return (content_type, 0.95)
        
        # Check for personality indicators
        personality_indicators = [
            'shy', 'quiet', 'dominant', 'aggressive', 'resistant', 
            'difficult', 'expert', 'sme', 'personality',
            'commander', 'chief', 'nco', 'officer', 'airman',
            'resistant to change', 'by the book', 'old school'
        ]
        if any(term in query_lower for term in personality_indicators):
            return ('personality', 0.9)
        
        # Other patterns remain the same
        patterns = {
            'icebreaker': ['icebreaker', 'start session', 'begin meeting', 'warm up'],
            'brainstorming': ['brainstorm', 'ideate', 'generate ideas']
        }
        
        for category, terms in patterns.items():
            matches = sum(term in query_lower for term in terms)
            if matches:
                confidence = 0.8 * (matches / len(terms))
                if confidence > 0.6:
                    return (category, confidence)
        
        return ('general', 0.5)

    def _build_efficient_prompt(
        self,
        query_type: str,
        context: List[Dict],
        confidence: float
    ) -> str:
        """Build optimized prompt based on query type and confidence"""
        
        # Select appropriate response template
        template = self.response_templates.get(query_type, self.response_templates['general'])
        
        # Build context section
        context_str = self._format_context(context, query_type)
        
        # Combine with base prompt, adjusting for confidence
        if confidence < self.CONFIDENCE_THRESHOLD:
            prompt = f"{self.base_prompt}\n\nNOTE: Context is uncertain, consider asking for clarification.\n\n"
        else:
            prompt = f"{self.base_prompt}\n\n"
        
        prompt += f"CONTENT TYPE: {query_type}\n"
        prompt += f"RELEVANT CONTENT:\n{context_str}\n"
        prompt += f"RESPONSE FORMAT:\n{json.dumps(template['structure'], indent=2)}"
        
        return prompt

    def _get_enhanced_base_prompt(self) -> str:
        return """You are Chip, embodying the Stale Chips methodology and spirit.

CORE IDENTITY:
- We help humans make real change happen in the DoD
- Everything we share comes from trial and error, not theory
- We use subtle humor to build connection, not to entertain
- We understand DoD bureaucracy and barriers to change
- Results matter more than innovation theater

CONVERSATION STYLE:
1. Building Connection
   - Use subtle humor (dad jokes, self-deprecating, playful)
   - Start light, increase personality as rapport builds
   - Show DoD knowledge through natural references
   - Match user's military terminology level
   - Example good: "Sounds like someone needs a DFAC coffee break..."
   - Example bad: "As someone who understands military culture..."

2. Teaching Approach
   - Share what worked AND how it could fail
   - Encourage adaptation to their context
   - Always follow tool explanations with "What are you thinking?"
   - Connect answers to their scenario
   - Example good: "This worked great with the 42nd MSG, but you might want to adjust X for your group"
   - Example bad: "This should work in any military context"

3. Problem Solving Flow
   - Ask clarifying questions to understand context
   - Pull from multiple sources (tools, personalities, facilitation tips)
   - Share relevant anecdotes ONLY from our content
   - If content isn't found, double-check and be transparent
   - Default to "Let's find another way to help you" vs making up content

4. When We Don't Have Content
   Step 1: "Let me check again..."
   Step 2: "Hmm, I don't see that in my memory. Could you rephrase what you need?"
   Step 3: "Please reach out to the team directly at ramjet@stalechips.com"

RESPONSE GUIDELINES:
1. For Tools/Techniques
   - Name and quick overview
   - Materials needed
   - Video link (NO timestamps)
   - "What are you thinking about this for your situation?"

2. For Personality Management
   - Only reference DTIP course content
   - Share specific examples from our experience
   - Focus on practical application
   - Ask about their specific context

3. For General Questions
   - Start with clarifying questions
   - Pull relevant facilitation tips
   - Connect to their scenario
   - Encourage experimentation

Remember: 
1. Never make up content or examples
2. Never include timestamps
3. Only reference DTIP for personality management
4. Keep responses casual but focused on helping
5. Always encourage adaptation to their context"""

    def _build_prompt(self, query: str, content: Dict) -> str:
        """Build structured prompt with all relevant content"""
        prompt = f"""{self.base_prompt}

SPECIFIC TOOLS:
{json.dumps(content['tools'], indent=2)}

FACILITATION GUIDANCE:
{json.dumps(content['general_tips'], indent=2)}

VIDEO REFERENCES:
{json.dumps(content['videos'], indent=2)}

SOURCES:
{json.dumps(list(content['sources']), indent=2)}

Remember to:
1. If explaining a specific tool:
   - Provide clear step-by-step instructions
   - List required materials
   - Explain why it works
   - Include video references
2. Always include relevant facilitation tips
3. Maintain the casual Stale Chips style
4. Reference specific videos when available"""

        return prompt

    def _get_direct_content(self, query_type: str, query: str) -> List[Dict]:
        """Get content directly from structured data sources"""
        content = []
        
        # Get relevant content based on query type
        if query_type in self.course_prompts:
            content.extend([
                {
                    'type': query_type,
                    'content': item,
                    'source': 'structured'
                }
                for item in self.course_prompts[query_type]
            ])
        
        # Limit results to prevent context overflow
        return content[:self.MAX_CONTEXT_ITEMS]

    def _format_context(self, context: List[Dict], query_type: str) -> str:
        """Format context items into a string for the prompt"""
        if not context:
            return "No specific content found. Using general knowledge."
        
        formatted_items = []
        for item in context:
            if isinstance(item, dict):
                # Format based on content type
                if item.get('type') == 'tool':
                    formatted_items.append(
                        f"TOOL: {item.get('content', {}).get('name', 'Unnamed')}\n"
                        f"Description: {item.get('content', {}).get('description', 'No description')}\n"
                        f"URL: {item.get('content', {}).get('url', 'No URL')}\n"
                    )
                else:
                    # Generic formatting for other types
                    formatted_items.append(str(item.get('content', 'No content')))
        
        return "\n\n".join(formatted_items)