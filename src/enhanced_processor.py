import pandas as pd
import numpy as np
from typing import Dict, List, Set, Optional
import os
import json
import re

class EnhancedContentProcessor:
    def __init__(self):
        self.context_patterns = {
            'group_size': r'(\d+[-\s]?)+\s*participants?',
            'time_required': r'(\d+[-\s]?)+\s*minutes?',
            'complexity_indicators': [
                'easy', 'medium', 'hard', 'simple', 'complex',
                'straightforward', 'challenging'
            ]
        }
        
        # Key facilitation principles extracted from content
        self.facilitation_principles = {
            'engagement': ['discussion', 'conversation', 'share', 'participate'],
            'clarity': ['explain', 'describe', 'demonstrate', 'show'],
            'support': ['help', 'guide', 'assist', 'facilitate'],
            'time_management': ['quick', 'fast', 'efficient', 'time']
        }
        
        # Tool relationships and prerequisites
        self.tool_relationships = {}
        
    def process_content(self, input_dir: str, output_dir: str):
        """Process all content files."""
        print("Starting enhanced content processing...")
        
        # Process course files
        unified_content = self._process_course_files(input_dir)
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Save processed content
        output_path = os.path.join(output_dir, 'unified_content.csv')
        unified_content.to_csv(output_path, index=False)
        print(f"Saved processed content to {output_path}")
    
    def _process_course_files(self, input_dir: str) -> pd.DataFrame:
        """Process individual course files with context awareness."""
        all_data = []
        
        for file in os.listdir(input_dir):
            if file.endswith('.csv') and not file.startswith('.'):
                file_path = os.path.join(input_dir, file)
                try:
                    df = self._process_single_file(file_path)
                    all_data.append(df)
                    print(f"Successfully processed {file}")
                except Exception as e:
                    print(f"Error processing {file}: {str(e)}")
        
        return pd.concat(all_data, ignore_index=True)
    
    def _process_single_file(self, file_path: str) -> pd.DataFrame:
        """Process single course file with enhanced understanding."""
        df = pd.read_csv(file_path)
        course_name = self._extract_course_name(file_path)
        
        # Extract rich metadata
        df['course'] = course_name
        df['extracted_contexts'] = df['Description'].apply(self._extract_contexts)
        df['key_concepts'] = df.apply(
            lambda x: self._extract_key_concepts(x['Description'], x['Transcription']),
            axis=1
        )
        df['facilitation_tips'] = df['Transcription'].apply(self._extract_facilitation_tips)
        
        return df
    
    def _extract_contexts(self, text: str) -> Dict:
        """Extract rich context from text."""
        contexts = {
            'group_size': None,
            'time_required': None,
            'complexity': None,
            'prerequisites': [],
            'best_practices': []
        }
        
        if isinstance(text, str):
            # Extract group size
            size_match = re.search(self.context_patterns['group_size'], text)
            if size_match:
                contexts['group_size'] = size_match.group()
            
            # Extract time required
            time_match = re.search(self.context_patterns['time_required'], text)
            if time_match:
                contexts['time_required'] = time_match.group()
            
            # Extract complexity
            for indicator in self.context_patterns['complexity_indicators']:
                if indicator.lower() in text.lower():
                    contexts['complexity'] = indicator
                    break
        
        return json.dumps(contexts)
    
    def _extract_facilitation_tips(self, text: str) -> List[str]:
        """Extract facilitation tips from transcription."""
        tips = []
        
        if isinstance(text, str):
            # Look for key phrases that indicate facilitation guidance
            sentences = text.split('.')
            for sentence in sentences:
                # Check if sentence contains facilitation principles
                for principle, keywords in self.facilitation_principles.items():
                    if any(keyword in sentence.lower() for keyword in keywords):
                        tips.append(sentence.strip())
                        break
        
        return json.dumps(tips)
    
    def _build_tool_relationships(self, df: pd.DataFrame):
        """Build understanding of tool relationships."""
        for idx, row in df.iterrows():
            tool_name = row['Name']
            self.tool_relationships[tool_name] = {
                'prerequisites': self._find_prerequisites(row),
                'complementary_tools': self._find_complementary_tools(row, df),
                'use_cases': self._extract_use_cases(row)
            }
    
    def _find_prerequisites(self, row: pd.Series) -> List[str]:
        """Identify prerequisites for a tool."""
        prerequisites = []
        if isinstance(row['Materials'], str):
            if 'previous' in row['Materials'].lower():
                prerequisites.append('Prior brainstorming')
        return prerequisites
    
    def _find_complementary_tools(self, row: pd.Series, df: pd.DataFrame) -> List[str]:
        """Identify tools that work well together."""
        complementary = []
        if isinstance(row['Description'], str):
            for idx, other_row in df.iterrows():
                if row['Name'] != other_row['Name']:
                    if other_row['Name'].lower() in row['Description'].lower():
                        complementary.append(other_row['Name'])
        return complementary
    
    def _extract_use_cases(self, row: pd.Series) -> List[str]:
        """Extract specific use cases for a tool."""
        use_cases = []
        if isinstance(row['When to use it?'], str):
            cases = row['When to use it?'].split('.')
            use_cases.extend([case.strip() for case in cases if case.strip()])
        return use_cases
    
    def _enhance_with_context(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add contextual understanding to the dataset."""
        # Add relationship data
        df['tool_relationships'] = df['Name'].apply(
            lambda x: json.dumps(self.tool_relationships.get(x, {}))
        )
        
        return df
    
    def _save_processed_data(self, df: pd.DataFrame, output_dir: str):
        """Save processed data with all enhancements."""
        # Save main content
        output_path = os.path.join(output_dir, 'unified_content.csv')
        df.to_csv(output_path, index=False)
        
        # Save relationships separately for quick access
        relationships_path = os.path.join(output_dir, 'tool_relationships.json')
        with open(relationships_path, 'w') as f:
            json.dump(self.tool_relationships, f, indent=2)
        
        print(f"Saved enhanced content to {output_path}")
        print(f"Saved tool relationships to {relationships_path}")
    
    def _extract_course_name(self, filename: str) -> str:
        """Extract course name from filename."""
        # Remove extension and sheet suffix
        base_name = filename.replace('.csv', '').replace(' - Sheet1', '')
        return base_name.strip()

if __name__ == "__main__":
    # Define paths
    base_dir = '/users/johnnysaye/desktop/testproject/spiciest_chip'
    input_dir = os.path.join(base_dir, 'data/raw_courses')
    output_dir = os.path.join(base_dir, 'data/processed')
    
    # Process content
    processor = EnhancedContentProcessor()
    processor.process_content(input_dir, output_dir)