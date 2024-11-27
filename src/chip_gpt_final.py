import os
from typing import Dict, List
import anthropic
from dotenv import load_dotenv
import faiss
import numpy as np
import pandas as pd
from datetime import datetime

class ChipGPT:
    def __init__(self, data_dir: str):
        # Load environment variables
        load_dotenv()
        
        # Initialize Anthropic client
        self.client = anthropic.Anthropic()
        
        # Load and process content
        self.content_df = pd.read_csv(os.path.join(data_dir, 'raw_courses/Prioritization Tools - Sheet1.csv'))
        self.setup_vector_store()
        
    def setup_vector_store(self):
        """Initialize FAISS vector store with content embeddings."""
        self.index = faiss.IndexFlatL2(1536)  # Claude's embedding dimension
        self.content_map = {}
        
        # Process each tool
        for idx, row in self.content_df.iterrows():
            # Create rich text for embedding
            content = f"Tool: {row['Name']}\nDescription: {row['Description']}\nUse Case: {row['When to use it?']}\nTranscript: {row['Transcription']}"
            
            # Get embedding
            embedding = self._get_embedding(content)
            
            # Add to FAISS
            self.index.add(np.array([embedding]))
            
            # Store content mapping
            self.content_map[idx] = {
                'name': row['Name'],
                'description': row['Description'],
                'use_case': row['When to use it?'],
                'url': row['URL of Video Training'],
                'complexity': row['Complexity'],
                'participants': row['Number of Participants'],
                'time_needed': row['Length of Time']
            }
    
    def _get_embedding(self, text: str) -> np.ndarray:
        """Get embedding from Claude API."""
        try:
            response = self.client.embeddings.create(
                model="claude-3-opus-20240229",
                input=text
            )
            return response.embeddings[0]
        except Exception as e:
            print(f"Embedding error: {str(e)}")
            return np.zeros(1536)

    def process_query(self, query: str) -> str:
        """Process user query with relevant content."""
        try:
            # Get query embedding
            query_embedding = self._get_embedding(query)
            
            # Search for relevant content
            D, I = self.index.search(np.array([query_embedding]), k=2)
            
            # Get relevant content
            relevant_content = [self.content_map[i] for i in I[0]]
            
            # Build prompt with context
            prompt = self._build_prompt(query, relevant_content)
            
            # Get response from Claude
            response = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}],
                system=self._get_system_prompt()
            )
            
            return response.content
            
        except Exception as e:
            print(f"Error processing query: {str(e)}")
            return "I apologize, but I'm having trouble processing your request."
    
    def _build_prompt(self, query: str, relevant_content: List[Dict]) -> str:
        """Build prompt with relevant context."""
        context_parts = []
        
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

Remember to:
1. Be conversational and engaging
2. Draw from our specific tools and experience
3. Only mention tools and videos if truly relevant
4. Focus on practical guidance
5. Keep our unique facilitation style

Respond as an experienced facilitator would."""

        return prompt
    
    def _get_system_prompt(self) -> str:
        return """You are Chip, an expert facilitator who has run workshops for everyone from Airmen to admirals. You maintain a conversational yet authoritative style while drawing from real experience. You focus on practical application over theory and use examples from actual workshops. Make responses engaging and natural, like getting advice from an experienced colleague."""