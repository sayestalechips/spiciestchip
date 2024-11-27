import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.chip_gpt_v2 import ChipGPT
import logging
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_cli():
    try:
        load_dotenv()
        content_dir = os.path.join('data', 'processed')
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