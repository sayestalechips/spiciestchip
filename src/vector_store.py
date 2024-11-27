from openai import OpenAI
import numpy as np
from typing import List, Dict
import faiss
import pickle
import logging
import os
from dotenv import load_dotenv

load_dotenv(override=True)
logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self, dimension: int = 1536):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.content_store = {}
        
        # Initialize OpenAI client
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        if not self.client.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
    def _get_embeddings(self, texts: List[str]) -> np.ndarray:
        """Get embeddings from OpenAI API with batching."""
        embeddings = []
        batch_size = 10  # Adjust batch size as needed
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            try:
                logger.info(f"Processing batch {i//batch_size + 1} of {(len(texts) + batch_size - 1)//batch_size}")
                
                # New API call syntax
                response = self.client.embeddings.create(
                    input=batch,
                    model="text-embedding-ada-002"
                )
                
                # New response structure
                batch_embeddings = [item.embedding for item in response.data]
                embeddings.extend(batch_embeddings)
                
            except Exception as e:
                logger.error(f"Error getting embeddings for batch {i//batch_size + 1}: {e}")
                raise
            
        return np.array(embeddings)
    
    def add_content(self, texts: List[str], metadata: List[Dict]):
        """Add content to vector store with metadata."""
        # Get embeddings from OpenAI
        embeddings = self._get_embeddings(texts)
        
        # Add to FAISS index
        self.index.add(embeddings)
        
        # Store metadata
        start_idx = len(self.content_store)
        for i, meta in enumerate(metadata):
            self.content_store[start_idx + i] = {
                'content': texts[i],
                'metadata': meta
            }
            
    def search(self, query: str, k: int = 5) -> List[Dict]:
        """Search for relevant content."""
        query_embedding = self._get_embeddings([query])[0].reshape(1, -1)
        D, I = self.index.search(query_embedding, k)
        results = []
        for idx in I[0]:
            if idx in self.content_store:
                results.append(self.content_store[idx])
        return results
    
    def save(self, path: str):
        """Save vector store to disk."""
        save_dict = {
            'dimension': self.dimension,
            'content_store': self.content_store
        }
        
        # Save FAISS index
        faiss.write_index(self.index, f"{path}.faiss")
        
        # Save metadata
        with open(f"{path}.meta", 'wb') as f:
            pickle.dump(save_dict, f)
            
    @classmethod
    def load(cls, path: str) -> 'VectorStore':
        """Load vector store from disk."""
        # Load metadata
        with open(f"{path}.meta", 'rb') as f:
            save_dict = pickle.load(f)
            
        # Create instance
        store = cls(dimension=save_dict['dimension'])
        store.content_store = save_dict['content_store']
        
        # Load FAISS index
        store.index = faiss.read_index(f"{path}.faiss")
        
        return store
    
    def _create_tool_text(self, row):
        """Create formatted text from a row."""
        try:
            # Add URL to the formatted text
            return f"""Tool: {row['Name']}
                    Complexity: {row['Complexity']}
                    Participants: {row['Number of Participants']}
                    Materials: {row['Materials']}
                    Duration: {row['Length of Time']}
                    Description: {row['Description']}
                    When to use: {row['When to use it?']}
                    Video Link: {row.get('URL of Video Training', 'No video available')}
                    """
        except Exception as e:
            logger.error(f"Error creating tool text: {e}")
            raise