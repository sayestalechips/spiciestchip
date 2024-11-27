from chip_gpt import ChipGPT  # Using v1 instead of v2 for now
import os
import logging
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_cli():
    try:
        # Load environment variables including API key
        load_dotenv()
        
        # Initialize ChipGPT
        content_dir = os.path.join(os.path.dirname(__file__), '..', 'data/processed')
        os.makedirs(content_dir, exist_ok=True)
        
        logger.info("Initializing ChipGPT...")
        chip = ChipGPT(content_dir)
        
        print("\nWelcome to Chip! Type 'exit' to quit.\n")
        
        while True:
            query = input("You: ").strip()
            
            if query.lower() == 'exit':
                print("\nThanks for chatting! Goodbye!\n")
                break
            
            print("-" * 50)
            try:
                response = chip.process_query(query)
                print(f"\nChip: {response}\n")
            except Exception as e:
                logger.error(f"Error: {str(e)}")
                print(f"Sorry, I encountered an error: {str(e)}\n")
            print("-" * 50)

    except Exception as e:
        logger.error(f"Startup failed: {str(e)}")
        raise

if __name__ == "__main__":
    run_cli()