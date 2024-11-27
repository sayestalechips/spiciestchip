import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from chip_gpt import ChipGPT

def main():
    # Initialize ChipGPT
    content_dir = os.path.join(os.path.dirname(__file__), 'data/processed')
    chip = ChipGPT(content_dir)
    
    # Test queries
    test_queries = [
        "I need help making my team more creative",
        "Tell me about Impact over Easy",
        "I have a group of 12 people and need to prioritize ideas quickly"
    ]
    
    # Process each query
    for query in test_queries:
        print(f"\nQuery: {query}")
        print("-" * 50)
        response = chip.process_query(query)
        print(f"Response: {response}\n")
        print("-" * 50)

if __name__ == "__main__":
    main()