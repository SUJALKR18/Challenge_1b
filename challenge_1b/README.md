# Adobe Challenge 1b - Intelligent Document Analysis System

A sophisticated document analysis system that processes PDF collections to extract relevant sections based on user personas and tasks. The system uses advanced NLP techniques including semantic embeddings and relevance ranking to provide intelligent document insights.

## 🚀 Features

- **Multi-PDF Processing**: Handles collections of PDF documents with parallel processing
- **Semantic Search**: Uses sentence-transformers for intelligent content matching
- **Relevance Ranking**: Advanced ranking algorithm with top-K aggregation
- **Structured Output**: Generates clean JSON output with top 5 most relevant sections
- **Fast Performance**: Optimized to complete processing in under 60 seconds
- **Modular Architecture**: Clean, maintainable codebase with separated concerns

## 📁 Project Structure

```
app_pr/
├── main.py                      # Main execution script
├── data_structures.py           # Core data classes and types
├── utils.py                     # Utility functions and constants
├── core/                        # Core system components
│   ├── document_parser.py       # PDF parsing and structure extraction
│   ├── embedding_engine.py      # Text embedding and chunking
│   ├── ranking_engine.py        # Relevance scoring and ranking
│   └── output_builder.py        # JSON output generation
└── Challenge_1b/                # Data directory
    ├── Collection_1/            # Travel planning documents
    ├── Collection_2/            # HR forms documents
    └── Collection_3/            # Menu planning documents
```

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Dependencies
The system automatically downloads required models and dependencies on first run:

```bash
# Core dependencies (installed automatically)
- sentence-transformers    # For text embeddings
- PyMuPDF (fitz)          # For PDF processing
- nltk                    # For text tokenization
- numpy                   # For numerical operations
- scikit-learn           # For cosine similarity
```

## 🚀 How to Run This Project

### Prerequisites Check
First, ensure you have Python 3.8+ installed:
```bash
python --version
```

### Step 1: Navigate to Project Directory
```bash
cd app_pr
```

### Step 2: Run the System
Choose one of the available collections:

#### Option A: Run Collection 1 (Travel Planning)
```bash
python main.py Collection_1
```

#### Option B: Run Collection 2 (HR Forms)
```bash
python main.py Collection_2
```

#### Option C: Run Collection 3 (Menu Planning)
```bash
python main.py Collection_3
```

### Step 3: Check Results
After processing, check the output file:
```bash
# View the generated output
cat Challenge_1b/Collection_1/challenge1b_output.json
```

### Advanced Usage
Specify a custom embedding model:

```bash
python main.py Collection_1 --model_path "sentence-transformers/all-MiniLM-L6-v2"
```

### Expected Output
- **Processing Time**: < 60 seconds
- **Output Location**: `Challenge_1b/Collection_X/challenge1b_output.json`
- **Format**: Clean JSON with top 5 relevant sections

### Troubleshooting
If you encounter issues:
1. **Model Download**: The system automatically downloads required models on first run
2. **PDF Files**: Ensure all PDF files exist in the `Challenge_1b/Collection_X/PDFs/` directory
3. **Input Format**: Verify `challenge1b_input.json` follows the correct format
4. **Permissions**: Ensure you have read/write permissions in the project directory

## 📊 Input Format

Each collection requires a `challenge1b_input.json` file:

```json
{
    "documents": [
        {"filename": "document1.pdf"},
        {"filename": "document2.pdf"}
    ],
    "persona": {
        "role": "Travel Planner"
    },
    "job_to_be_done": {
        "task": "Plan a trip of 4 days for a group of 10 college friends."
    }
}
```

## 📤 Output Format

The system generates `challenge1b_output.json` with the following structure:

```json
{
    "metadata": {
        "input_documents": ["document1.pdf", "document2.pdf"],
        "persona": "Travel Planner",
        "job_to_be_done": "Plan a trip of 4 days for a group of 10 college friends.",
        "processing_timestamp": "2025-07-28T20:17:12"
    },
    "extracted_sections": [
        {
            "document": "document1.pdf",
            "section_title": "Page 8",
            "importance_rank": 1,
            "page_number": 8
        }
    ],
    "subsection_analysis": [
        {
            "document": "document1.pdf",
            "refined_text": "Cleaned and formatted content...",
            "page_number": 8
        }
    ]
}
```

## 🔧 System Architecture

### Core Components

1. **Document Parser** (`core/document_parser.py`)
   - Extracts text and structure from PDFs
   - Handles Table of Contents (ToC) or falls back to page-based sectioning
   - Uses PyMuPDF for efficient PDF processing

2. **Embedding Engine** (`core/embedding_engine.py`)
   - Singleton pattern for model management
   - Text chunking with sentence overlap
   - Generates dense vector embeddings using sentence-transformers

3. **Ranking Engine** (`core/ranking_engine.py`)
   - Calculates cosine similarity between query and text chunks
   - Aggregates chunk scores to section scores (Mean of Top-K strategy)
   - Performs global ranking and sub-section analysis

4. **Output Builder** (`core/output_builder.py`)
   - Formats processed data into structured JSON
   - Cleans text formatting and removes excessive newlines
   - Ensures output conforms to required specifications

### Data Structures

- **Chunk**: Individual text segments with embeddings
- **Section**: Document sections containing multiple chunks
- **Document**: Complete PDF with multiple sections
- **SystemInput**: Input configuration (persona, task, PDF paths)
- **FinalOutput**: Structured output with metadata and results

## ⚡ Performance Optimizations

- **Parallel Processing**: Uses ProcessPoolExecutor for concurrent PDF processing
- **Model Caching**: Sentence-transformers automatically caches downloaded models
- **Limited Workers**: Restricts to 4 processes to avoid overhead
- **Efficient Chunking**: Optimized text segmentation with sentence overlap
- **Memory Management**: Processes documents in parallel without memory bloat

## 🎯 Key Features

### Intelligent Ranking
- **Semantic Matching**: Uses advanced embeddings for content understanding
- **Top-K Aggregation**: Combines multiple chunk scores for robust section ranking
- **Global Ranking**: Ranks all sections across all documents
- **Sub-section Analysis**: Provides detailed analysis of top 5 sections

### Text Processing
- **Smart Chunking**: Splits text at sentence boundaries with overlap
- **Content Cleaning**: Removes excessive formatting and newlines
- **Structured Output**: Maintains document hierarchy and page numbers

### Error Handling
- **Graceful Degradation**: Falls back to page-based sectioning if ToC unavailable
- **File Validation**: Checks for PDF existence and accessibility
- **Exception Handling**: Robust error handling for individual document processing

## 📈 Performance Metrics

- **Processing Time**: < 60 seconds per collection
- **Memory Usage**: Optimized for large document collections
- **Accuracy**: High relevance ranking through semantic understanding
- **Scalability**: Parallel processing supports multiple documents

## 🔍 Example Use Cases

1. **Travel Planning**: Extract relevant travel tips and recommendations
2. **HR Documentation**: Find relevant forms and procedures for onboarding
3. **Menu Planning**: Identify suitable recipes and meal suggestions
4. **Research Analysis**: Extract key insights from research papers
5. **Legal Document Review**: Find relevant sections in legal documents

## 🛠️ Development

### Adding New Collections
1. Create a new directory in `Challenge_1b/`
2. Add PDF files to the `PDFs/` subdirectory
3. Create `challenge1b_input.json` with proper format
4. Run: `python main.py Collection_Name`

### Customizing Models
- Change the default model in `utils.py`
- Specify custom models via command line argument
- Supported: Any sentence-transformers model

### Extending Functionality
- Add new ranking algorithms in `ranking_engine.py`
- Implement custom text processing in `embedding_engine.py`
- Modify output format in `output_builder.py`

## 📝 License

This project is developed for Adobe Challenge 1b.

## 🤝 Contributing

The system is designed with modularity in mind, making it easy to extend and improve:
- Add new embedding models
- Implement different ranking algorithms
- Enhance text processing capabilities
- Optimize performance further

---

**Built with ❤️ for intelligent document analysis** 