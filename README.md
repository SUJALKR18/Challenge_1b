# Challenge 1B - PDF Document Processing System

An advanced NLP system for processing PDF documents using semantic embeddings and intelligent ranking algorithms.

## Features

- **PDF Document Parsing**: Extracts text and structure from PDF files
- **Semantic Embeddings**: Uses sentence-transformers for vector representations
- **Intelligent Ranking**: Ranks document sections based on relevance to user queries
- **Multi-Collection Processing**: Handles multiple document collections
- **Parallel Processing**: Utilizes multiprocessing for efficient document processing

## Quick Start with Docker

### Prerequisites

- Docker Desktop installed and running
- At least 4GB of available RAM

### Build and Run

1. **Build the Docker image:**
   ```bash
   docker build -t challenge-1b:latest .
   ```

2. **Run a collection:**
   ```bash
   # Process Collection_1 (South of France travel guides)
   docker run --rm \
     -v "$(pwd)/challenge_1b/Datasets:/app/challenge_1b/Datasets" \
     challenge-1b:latest \
     python challenge_1b/main.py Collection_1
   
   # Process Collection_2 (Adobe Acrobat documentation)
   docker run --rm \
     -v "$(pwd)/challenge_1b/Datasets:/app/challenge_1b/Datasets" \
     challenge-1b:latest \
     python challenge_1b/main.py Collection_2
   
   # Process Collection_3 (Recipe collections)
   docker run --rm \
     -v "$(pwd)/challenge_1b/Datasets:/app/challenge_1b/Datasets" \
     challenge-1b:latest \
     python challenge_1b/main.py Collection_3
   ```

### Using Docker Compose

```bash
# Start the container
docker-compose up -d

# Execute a command
docker-compose exec challenge-1b python challenge_1b/main.py Collection_1

# Stop the container
docker-compose down
```

## Available Collections

- **Collection_1**: South of France travel guides (cities, cuisine, history, etc.)
- **Collection_2**: Adobe Acrobat documentation and tutorials
- **Collection_3**: Recipe collections (breakfast, lunch, dinner ideas)

## Output

The system generates `challenge1b_output.json` files in each collection directory containing:
- Extracted relevant sections
- Sub-section analysis
- Processing metadata
- Relevance scores and rankings

## Methodology

For detailed information about the system's approach and methodology, see [approach_explanation.md](approach_explanation.md).

## Troubleshooting

### Common Issues

1. **Docker not running:**
   ```bash
   docker info
   ```

2. **Out of memory errors:**
   - Increase Docker memory limit in Docker Desktop settings
   - Recommended: 4GB minimum, 8GB preferred

3. **Permission issues on Windows:**
   - Ensure Docker Desktop has access to the project directory
   - Use Windows-style paths if needed

### Cleanup

```bash
# Remove Docker images
docker rmi challenge-1b:latest

# Clean up system
docker system prune -f
```

## Development

For development without Docker:

1. Install Python 3.11+
2. Install dependencies: `pip install -r requirements.txt`
3. Download NLTK data: `python -c "import nltk; nltk.download('punkt')"`
4. Run: `python challenge_1b/main.py Collection_1`
