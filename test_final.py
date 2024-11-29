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
        
        logger.info("Initializing ChipGPT with enhanced query processing...")
        chip = ChipGPT(content_dir)
        
        print("\nWelcome to Chip! Type 'exit' to quit.")
        print("Special commands:")
        print("- 'debug': Show query classification details")
        print("- 'verbose': Toggle verbose mode for seeing content sources\n")
        
        verbose_mode = False
        
        while True:
            query = input("You: ").strip()
            
            if query.lower() == 'exit':
                print("\nThanks for chatting! Goodbye!\n")
                break
                
            if query.lower() == 'verbose':
                verbose_mode = not verbose_mode
                print(f"\nVerbose mode: {'ON' if verbose_mode else 'OFF'}\n")
                continue
                
            print("-" * 50)
            try:
                if verbose_mode:
                    logger.info("Processing query...")
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