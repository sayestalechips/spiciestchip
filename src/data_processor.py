import pandas as pd
import os
from typing import Dict, List

class DataProcessor:
    def __init__(self):
        self.column_mappings = {
            'Name': ['name', 'tool_name', 'tool'],
            'Complexity': ['complexity', 'difficulty'],
            'Number of Participants': ['participants', 'group_size', 'number_of_participants'],
            'Materials': ['materials', 'required_materials'],
            'Length of Time': ['time', 'duration', 'length_of_time'],
            'Description': ['description', 'what_is_it'],
            'URL of Video Training': ['url', 'video_url', 'training_url'],
            'When to use it?': ['when_to_use', 'use_case', 'best_for'],
            'Transcription': ['transcription', 'transcript']
        }
        
    def standardize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize column names across different CSV formats."""
        standardized = df.copy()
        
        for standard_name, variations in self.column_mappings.items():
            for variant in variations:
                if variant in df.columns:
                    standardized = standardized.rename(columns={variant: standard_name})
                    break
                    
        return standardized
    
    def process_course_file(self, file_path: str) -> pd.DataFrame:
        """Process a single course file."""
        # Extract course name from filename
        course_name = os.path.basename(file_path).replace(' - Sheet1.csv', '')
        
        # Read CSV
        df = pd.read_csv(file_path)
        
        # Standardize columns
        df = self.standardize_columns(df)
        
        # Add course name column
        df['course_category'] = course_name
        
        return df
    
    def process_all_courses(self, input_dir: str, output_path: str):
        """Process all course files and create unified CSV."""
        all_data = []
        
        # Process each course file
        for file in os.listdir(input_dir):
            if file.endswith('.csv') and not file.startswith('.'):
                file_path = os.path.join(input_dir, file)
                try:
                    df = self.process_course_file(file_path)
                    all_data.append(df)
                except Exception as e:
                    print(f"Error processing {file}: {str(e)}")
        
        # Combine all data
        unified_df = pd.concat(all_data, ignore_index=True)
        
        # Save unified data
        unified_df.to_csv(output_path, index=False)
        print(f"Unified data saved to {output_path}")
        return unified_df