from chip_gpt_v2 import ChipGPT

def main():
    print("Initializing Chip...")
    chip = ChipGPT("data/processed/vector_store")
    
    print("\nHey! I'm Chip. How can I help you with facilitation today?")
    
    while True:
        # Get input from user
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("\nThanks for chatting! Take care!")
            break
            
        # Process query and get response
        response = chip.process_query(user_input)
        print(f"\nChip: {response}")

if __name__ == "__main__":
    main()