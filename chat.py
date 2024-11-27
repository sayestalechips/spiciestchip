import os
import sys
from dotenv import load_dotenv
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from chip_gpt_v2 import ChipGPT

def main():
    # Load environment variables (including API key)
    load_dotenv()
    
    # Initialize directories
    content_dir = os.path.join(os.path.dirname(__file__), 'data/processed')
    os.makedirs(content_dir, exist_ok=True)
    
    print("\nInitializing Chip...\n")
    chip = ChipGPT(content_dir)
    
    print("Hey! I'm Chip, your facilitation assistant. What can I help you with today?")
    print("(Type 'exit' to end the conversation)\n")
    
    while True:
        # Get user input
        user_input = input("You: ").strip()
        
        if user_input.lower() in ['exit', 'quit']:
            print("\nThanks for chatting! Take care!")
            break
            
        # Process query and get response
        response = chip.process_query(user_input)
        print(f"\nChip: {response}\n")