from content_processor_v2 import ContentProcessor

def main():
    print("Starting content processing...")
    processor = ContentProcessor()
    
    # Process content and create vector store
    vector_store = processor.process_content("data/raw_courses")
    
    # Save vector store
    print("Saving vector store...")
    vector_store.save("data/processed/vector_store")
    print("Done!")

if __name__ == "__main__":
    main()