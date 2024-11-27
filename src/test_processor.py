from data_processor import DataProcessor
import os

def test_single_file():
    # Setup paths
    base_dir = '/users/johnnysaye/desktop/testproject/spiciest_chip'
    test_file = os.path.join(base_dir, 'data/raw_courses/Prioritization Tools - Sheet1.csv')
    
    # Process single file
    processor = DataProcessor()
    df = processor.process_course_file(test_file)
    
    # Print results
    print("\nProcessed columns:", df.columns.tolist())
    print("\nFirst tool info:")
    print(df.iloc[0])