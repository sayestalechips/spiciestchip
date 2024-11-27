import os
from pathlib import Path

# Project root directory (2 levels up from this file)
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Data paths
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw_courses")
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")
VECTOR_STORE_PATH = os.path.join(PROCESSED_DATA_DIR, "vector_store")

# Vector store settings
EMBEDDING_DIMENSION = 1536  # Claude's embedding dimension
CHUNK_SIZE = 1000  # Size for text chunking
SEARCH_TOP_K = 5  # Number of relevant contents to retrieve

# Model settings
MODEL_NAME = "claude-3-opus-20240229"
MAX_TOKENS = 1024

# Ensure directories exist
os.makedirs(RAW_DATA_DIR, exist_ok=True)
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
