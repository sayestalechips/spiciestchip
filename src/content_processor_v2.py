from typing import List, Dict, Tuple
import pandas as pd
import os
import logging
from vector_store import VectorStore
from langchain.text_splitter import RecursiveCharacterTextSplitter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContentProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1500,
            chunk_overlap=300,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        # Initialize vector store
        self.vector_store = VectorStore()
        
        # Map all possible column names
        self.name_columns = ['Name', 'Name of Video', 'Name of Icebreaker Tool']
        self.description_columns = ['Description', 'Overview of Tool']
        self.complexity_columns = ['Complexity', 'Complexity of Tool']
        self.when_columns = ['When to use it?', 'When to use it ?']
        self.materials_columns = ['Materials']
        self.participants_columns = ['Number of Participants']
        self.duration_columns = ['Length of Time']

    def process_content(self, data_dir: str) -> VectorStore:
        """Process content from data directory."""
        documents = []
        total_files = len([f for f in os.listdir(data_dir) if f.endswith('.csv')])
        processed_files = 0
        
        for file in os.listdir(data_dir):
            if file.endswith('.csv'):
                processed_files += 1
                logger.info(f"Processing file {processed_files}/{total_files}: {file}")
                
                try:
                    df = pd.read_csv(os.path.join(data_dir, file))
                    logger.info(f"Successfully read {file}")
                    logger.info(f"Columns in file: {list(df.columns)}")
                    
                    # Process each row
                    for _, row in df.iterrows():
                        try:
                            text = self._create_tool_text(row)
                            metadata = self._create_metadata(row)
                            documents.append({
                                'text': text,
                                'metadata': metadata
                            })
                        except Exception as e:
                            logger.error(f"Error processing row: {e}")
                            continue
                            
                except Exception as e:
                    logger.error(f"Error processing file {file}: {e}")
                    continue

        return self._create_vector_store(documents)

    def _get_value(self, row, possible_columns):
        """Try to get value from multiple possible column names."""
        for col in possible_columns:
            if col in row:
                return row[col]
        return "Not specified"

    def _create_tool_text(self, row):
        """Create formatted text from a row."""
        try:
            return f"""Tool: {self._get_value(row, self.name_columns)}
Description: {self._get_value(row, self.description_columns)}
When to use: {self._get_value(row, self.when_columns)}
Setup: This tool needs {self._get_value(row, self.materials_columns)} and works with {self._get_value(row, self.participants_columns)}
Time Required: {self._get_value(row, self.duration_columns)}
"""
        except Exception as e:
            logger.error(f"Error creating tool text: {e}")
            raise

    def _create_metadata(self, row):
        """Create metadata dictionary from row."""
        return {
            'tool_name': self._get_value(row, self.name_columns),
            'complexity': self._get_value(row, self.complexity_columns),
            'participants': self._get_value(row, self.participants_columns),
            'duration': self._get_value(row, self.duration_columns),
            'use_case': self._get_value(row, self.when_columns),
            'materials': self._get_value(row, self.materials_columns),
        }

    def _create_vector_store(self, documents: List[Dict]):
        """Create vector store from processed documents."""
        texts = [doc["text"] for doc in documents]
        metadata = [doc["metadata"] for doc in documents]
        
        # Add to vector store
        print(f"Adding {len(texts)} content pieces to vector store...")
        self.vector_store.add_content(texts, metadata)
        
        return self.vector_store