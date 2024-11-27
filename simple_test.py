import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from chip_gpt import ChipGPT

def main():
    # Set up content directory path
    content_dir = os.path.join(os.path.dirname(__file__), 'data/processed')
    
    # Make sure the directory exists
    os.makedirs(content_dir, exist_ok=True)
    
    print("Initializing ChipGPT...")
    chip = ChipGPT(content_dir)
    
    # Test simple query
    test_query = "Tell me about facilitating workshops"
    print(f"\nTesting query: {test_query}")
    
    response = chip.process_query(test_query)
    print(f"\nResponse: {response}")

if __name__ == "__main__":
    main()