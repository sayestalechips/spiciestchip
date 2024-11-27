from data_processor import DataProcessor
import os

def main():
    # Setup paths
    base_dir = '/users/johnnysaye/desktop/testproject/spiciest_chip'
    input_dir = os.path.join(base_dir, 'data/raw_courses')
    output_dir = os.path.join(base_dir, 'data/processed')
    output_path = os.path.join(output_dir, 'unified_content.csv')
    
    # Create processor and process files
    processor = DataProcessor()
    unified_data = processor.process_all_courses(input_dir, output_path)
    print(f"Processed {len(unified_data)} tools across all courses")

if __name__ == "__main__":
    main()