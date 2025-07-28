"""
run_single_collection.py

This script processes a single collection by reading from its challenge1b_input.json file 
and generating the corresponding challenge1b_output.json file.

Usage:
    python run_single_collection.py Collection_1
    python run_single_collection.py Collection_2
    python run_single_collection.py Collection_3
"""

import os
import json
import time
import sys
import argparse
from pathlib import Path
from typing import Dict, List

# Import the existing system components
from data_structures import SystemInput
from core.document_parser import DocumentParser
from core.embedding_engine import EmbeddingEngine
from core.ranking_engine import RankingEngine
from core.output_builder import OutputBuilder

def process_single_pdf(pdf_path: str, model_path: str):
    """
    A top-level function designed to be run in a separate process.
    It parses a PDF, initializes its own embedding engine instance,
    and then chunks/embeds the content of the document.
    """
    # 1. Parse the document structure and text
    parser = DocumentParser(pdf_path)
    document = parser.parse()

    # 2. Initialize the embedding engine within this process
    embedder = EmbeddingEngine(model_path=model_path)

    # 3. Chunk and embed each section
    for section in document.sections:
        embedder.process_section(section)
        
    return document

def process_collection(collection_name: str, model_path: str = "thenlper/gte-small"):
    """
    Process a single collection by reading its input JSON and generating the output JSON.
    
    Args:
        collection_name (str): Name of the collection (e.g., "Collection_1")
        model_path (str): Path to the embedding model
    """
    collection_path = os.path.join("Challenge_1b", collection_name)
    
    if not os.path.exists(collection_path):
        print(f"Error: Collection directory not found: {collection_path}")
        return False
    
    print(f"\n{'='*60}")
    print(f"PROCESSING COLLECTION: {collection_name}")
    print(f"{'='*60}")
    
    # Read the input JSON file
    input_file = os.path.join(collection_path, "challenge1b_input.json")
    output_file = os.path.join(collection_path, "challenge1b_output.json")
    
    if not os.path.exists(input_file):
        print(f"Error: Input file not found at {input_file}")
        return False
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            input_data = json.load(f)
    except Exception as e:
        print(f"Error reading input file: {e}")
        return False
    
    # Extract information from input JSON
    documents = input_data.get("documents", [])
    persona = input_data.get("persona", {}).get("role", "")
    job_to_be_done = input_data.get("job_to_be_done", {}).get("task", "")
    # challenge_info = input_data.get("challenge_info", {})
    
    # Build PDF paths
    pdfs_dir = os.path.join(collection_path, "PDFs")
    pdf_paths = []
    
    for doc in documents:
        pdf_path = os.path.join(pdfs_dir, doc["filename"])
        if os.path.exists(pdf_path):
            pdf_paths.append(pdf_path)
        else:
            print(f"Warning: PDF file not found: {pdf_path}")
    
    if not pdf_paths:
        print(f"Error: No PDF files found in {pdfs_dir}")
        return False
    
    print(f"Found {len(pdf_paths)} PDF files to process")
    print(f"Persona: {persona}")
    print(f"Task: {job_to_be_done}")
    
    # Create system input
    system_input = SystemInput(
        pdf_paths=pdf_paths,
        persona=persona,
        job_to_be_done=job_to_be_done
    )
    
    # Initialize engines
    embedder = EmbeddingEngine(model_path=model_path)
    ranker = RankingEngine()
    output_builder = OutputBuilder(system_input)
    
    # Create query embedding
    query_text = f"Persona: {persona}. Task: {job_to_be_done}"
    query_embedding = embedder.embed_query(query_text)
    
    # Process documents in parallel
    from concurrent.futures import ProcessPoolExecutor, as_completed
    
    all_documents = []
    # Limit to 4 processes to avoid overhead
    with ProcessPoolExecutor(max_workers=4) as executor:
        future_to_pdf = {
            executor.submit(process_single_pdf, pdf_path, model_path): pdf_path 
            for pdf_path in pdf_paths
        }
        
        for future in as_completed(future_to_pdf):
            pdf_path = future_to_pdf[future]
            try:
                processed_document = future.result()
                all_documents.append(processed_document)
            except Exception as exc:
                print(f"'{os.path.basename(pdf_path)}' generated an exception: {exc}")
    
    # Rank and analyze
    ranked_sections = ranker.rank_sections_globally(all_documents, query_embedding)
    sub_section_analysis = ranker.perform_sub_section_analysis(ranked_sections)
    
    # Build output
    final_output = output_builder.build(ranked_sections, sub_section_analysis)
    
    # Add processing timestamp to metadata
    final_output.metadata["processing_timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    
    # Write output
    output_builder.write_to_file(final_output, output_file)
    
    print(f"Successfully processed {collection_name}")
    print(f"Output written to: {output_file}")
    return True

def main():
    """Main function to process a single collection."""
    parser = argparse.ArgumentParser(description="Process a single collection")
    parser.add_argument("collection_name", help="Name of the collection (e.g., Collection_1)")
    parser.add_argument("--model_path", default="thenlper/gte-small", help="Model name or path")
    
    args = parser.parse_args()
    
    start_time = time.time()
    
    # Check if collection exists
    collection_path = os.path.join("Challenge_1b", args.collection_name)
    if not os.path.exists(collection_path):
        print(f"Error: Collection '{args.collection_name}' not found at {collection_path}")
        print("Available collections:")
        challenge_dir = "Challenge_1b"
        if os.path.exists(challenge_dir):
            for item in os.listdir(challenge_dir):
                item_path = os.path.join(challenge_dir, item)
                if os.path.isdir(item_path) and item.startswith("Collection_"):
                    print(f"  - {item}")
        return
    
    # Process the collection
    try:
        success = process_collection(args.collection_name, args.model_path)
        if success:
            end_time = time.time()
            print(f"\n{'='*60}")
            print("PROCESSING COMPLETE")
            print(f"{'='*60}")
            print(f"Total execution time: {end_time - start_time:.2f} seconds")
        else:
            print(f"\nFailed to process {args.collection_name}")
    except Exception as e:
        print(f"Error processing {args.collection_name}: {e}")

if __name__ == "__main__":
    main() 