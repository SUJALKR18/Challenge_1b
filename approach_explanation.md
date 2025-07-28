# Methodology Explanation

## Overview

This project implements an advanced Natural Language Processing (NLP) system designed to process and analyze PDF documents using semantic understanding and intelligent ranking algorithms. The system follows a structured pipeline approach that combines document parsing, semantic embedding, and relevance ranking to extract meaningful information from document collections.

## Core Methodology

### 1. Document Structure-First Parsing

The system employs a "Structure-First" approach to PDF processing, prioritizing the extraction of document organization before content analysis. This methodology:

- **Table of Contents Extraction**: First attempts to identify and extract the document's Table of Contents (ToC) to understand the author's intended structure
- **Fallback Sectioning**: If no ToC is available, implements page-by-page sectioning to ensure comprehensive coverage
- **Hierarchical Organization**: Maintains the logical hierarchy of sections, subsections, and content blocks

This approach ensures that the semantic analysis respects the document's original organization, leading to more accurate content extraction and relevance assessment.

### 2. Semantic Embedding Pipeline

The system utilizes state-of-the-art sentence transformers to create dense vector representations of text content:

- **Model Selection**: Uses the `thenlper/gte-small` model, optimized for semantic similarity tasks
- **Chunking Strategy**: Implements paragraph-based text chunking with single-sentence overlap to maintain context
- **Normalized Embeddings**: Applies cosine normalization for improved similarity calculations
- **Query-Document Alignment**: Creates unified vector space for both user queries and document content

### 3. Intelligent Ranking System

The ranking engine implements a multi-stage relevance assessment:

- **Global Ranking**: Compares all document sections across the entire collection using cosine similarity
- **Sub-section Analysis**: Performs detailed analysis of individual chunks within sections
- **Score Aggregation**: Combines individual chunk scores to create section-level relevance metrics
- **Context Preservation**: Maintains relationships between related content across documents

### 4. Parallel Processing Architecture

To handle large document collections efficiently, the system implements:

- **Multiprocessing**: Uses ProcessPoolExecutor for parallel document processing
- **Resource Optimization**: Limits concurrent processes to prevent system overload
- **Memory Management**: Implements singleton patterns for heavy models to reduce memory footprint
- **Caching Strategy**: Persists model downloads and embeddings for improved performance

## Technical Implementation

### Data Structures

The system uses typed dataclasses to ensure data integrity:
- **Chunk**: Represents individual text segments with embeddings and metadata
- **Section**: Contains logical document sections with associated chunks
- **Document**: Represents complete PDF files with their section hierarchy
- **SystemInput**: Encapsulates user queries and processing parameters

### Processing Pipeline

1. **Input Processing**: Reads JSON configuration files specifying collections, personas, and tasks
2. **Document Parsing**: Extracts text and structure from PDF files using PyMuPDF
3. **Embedding Generation**: Creates semantic vectors for all text content
4. **Query Processing**: Generates embeddings for user queries (persona + task)
5. **Similarity Calculation**: Computes cosine similarity between queries and content
6. **Ranking and Analysis**: Performs multi-level relevance assessment
7. **Output Generation**: Creates structured JSON output with ranked sections and analysis

## Key Advantages

- **Scalability**: Handles multiple document collections with varying sizes and formats
- **Accuracy**: Combines structural and semantic understanding for precise content extraction
- **Flexibility**: Adapts to different document types and user personas
- **Performance**: Optimized for both speed and resource efficiency
- **Reproducibility**: Containerized deployment ensures consistent results across environments

This methodology provides a robust foundation for intelligent document processing, enabling users to quickly identify and extract relevant information from large document collections based on specific contexts and requirements. 