# Challenge 1b: Persona-Driven Document Intelligence

## 🎯 Overview
This solution acts as an intelligent document analyst that understands what matters to specific users. Given a collection of PDFs and a persona with a specific job-to-be-done, it extracts and ranks the most relevant sections and insights, making documents speak directly to user needs.

## 🧠 Approach & Implementation

### How It Works
1. **Document Processing**: Extracts text blocks from all PDFs using PyMuPDF, preserving page numbers and document structure
2. **Semantic Understanding**: Uses a lightweight sentence transformer (MiniLM) to convert text into meaningful embeddings
3. **Persona Alignment**: Embeds the user's persona and task description as a query vector
4. **Intelligent Ranking**: Computes semantic similarity between document sections and the persona's needs
5. **Insight Extraction**: Selects the most relevant sections and subsections, ranked by importance
6. **Structured Output**: Generates clean JSON with metadata, ranked sections, and refined text

### Key Features
- **Persona-Driven**: Understands different user types (researchers, students, professionals)
- **Task-Aware**: Focuses on specific jobs-to-be-done rather than generic content
- **Semantic Intelligence**: Uses advanced NLP to understand meaning, not just keywords
- **Multi-Document**: Processes collections of related documents together
- **Performance Optimized**: Handles 3-5 documents in under 60 seconds
- **Offline Operation**: Works completely offline with no internet dependencies

## 🛠️ Technical Implementation

### Libraries & Models Used
- **PyMuPDF (fitz)**: Fast, reliable PDF text extraction
- **sentence-transformers**: all-MiniLM-L6-v2 (~80MB) for semantic embeddings
- **numpy**: Efficient similarity calculations
- **Python Standard Library**: json, os, datetime for data handling

### Core Functions
- `extract_text_from_pdf()`: Extracts text blocks with page numbers
- `embed_text_blocks()`: Converts text to semantic embeddings
- `embed_persona_task()`: Creates query embedding from persona + task
- `rank_by_relevance()`: Ranks sections by semantic similarity
- `generate_output_json()`: Creates structured output with metadata

### Model Details
- **Model**: all-MiniLM-L6-v2 (sentence-transformers)
- **Size**: ~80MB (well under 1GB limit)
- **Performance**: Optimized for CPU inference
- **Accuracy**: State-of-the-art semantic similarity for English text

## 📦 Input/Output Format

### Input JSON Structure
```json
{
  "challenge_info": {
    "challenge_id": "round_1b_XXX",
    "test_case_name": "specific_test_case"
  },
  "documents": [
    {"filename": "doc1.pdf", "title": "Document Title"}
  ],
  "persona": {"role": "PhD Researcher in Computational Biology"},
  "job_to_be_done": {"task": "Prepare literature review on methodologies"}
}
```

### Output JSON Structure
```json
{
  "metadata": {
    "input_documents": ["doc1.pdf", "doc2.pdf"],
    "persona": "PhD Researcher in Computational Biology",
    "job_to_be_done": "Prepare literature review on methodologies",
    "processing_timestamp": "2025-07-28T10:30:00Z"
  },
  "extracted_sections": [
    {
      "document": "doc1.pdf",
      "section_title": "Methodology Overview",
      "importance_rank": 1,
      "page_number": 5
    }
  ],
  "subsection_analysis": [
    {
      "document": "doc1.pdf",
      "refined_text": "Detailed methodology description...",
      "page_number": 5,
      "importance_rank": 1
    }
  ]
}
```

## 🚀 Usage

### Docker Build
```bash
cd Challenge_1b
docker build --platform linux/amd64 -t persona-pdf-analyzer .
```

### Docker Run
```bash
# Example for Collection 1 (Travel Planning):
docker run --rm \
  -v $(pwd)/Collection\ 1/PDFs:/pdfs:ro \
  -v $(pwd)/Collection\ 1/challenge1b_input.json:/input.json:ro \
  -v $(pwd)/Collection\ 1:/outputs \
  persona-pdf-analyzer \
  --input_json /input.json \
  --pdf_dir /pdfs \
  --output_json /outputs/challenge1b_output.json
```

### Local Development
```bash
# Install dependencies
pip install PyMuPDF sentence-transformers numpy

# Run the script
python analyze_persona_docs.py \
  --input_json Collection\ 1/challenge1b_input.json \
  --pdf_dir Collection\ 1/PDFs \
  --output_json Collection\ 1/challenge1b_output.json
```

## 📊 Test Collections

### Collection 1: Travel Planning
- **Persona**: Travel Planner
- **Task**: Plan a 4-day trip for 10 college friends to South of France
- **Documents**: 7 travel guides covering cities, cuisine, history, etc.

### Collection 2: Adobe Acrobat Learning
- **Persona**: HR Professional
- **Task**: Create and manage fillable forms for onboarding and compliance
- **Documents**: 15 Acrobat tutorials and guides

### Collection 3: Recipe Collection
- **Persona**: Food Contractor
- **Task**: Prepare vegetarian buffet-style dinner menu for corporate gathering
- **Documents**: 9 cooking guides and recipe collections

## ✅ Testing & Validation

### Performance Metrics
- **Speed**: < 60 seconds for 3-5 documents
- **Memory**: < 1GB total (including model)
- **Accuracy**: High semantic relevance scores on test collections
- **Scalability**: Handles 3-10 documents efficiently

### Validation Checklist
- [x] Processes multiple document collections
- [x] Extracts relevant sections based on persona/task
- [x] Ranks sections by importance
- [x] Generates structured JSON output
- [x] Works offline (no internet required)
- [x] CPU-only operation
- [x] Model size within 1GB limit
- [x] Handles edge cases (missing files, empty docs)

## 🔧 Configuration

### Adjustable Parameters
- **Top N sections**: Number of most relevant sections to extract (default: 5)
- **Top N subsections**: Number of most relevant subsections (default: 5)
- **Similarity threshold**: Minimum similarity for relevance (built into ranking)
- **Text truncation**: Length limit for refined text (default: 500 chars)

### Model Customization
The solution uses a pre-trained model that works well across domains. For specialized use cases, you can:
- Fine-tune the model on domain-specific data
- Use different sentence transformer models
- Adjust embedding parameters

## 🐛 Troubleshooting

### Common Issues
1. **Low relevance scores**: Check if persona/task description is clear and specific
2. **Missing sections**: Ensure PDFs contain relevant content for the given task
3. **Model loading errors**: Verify sufficient disk space for model download
4. **Memory issues**: Reduce batch size or number of documents processed

### Debug Mode
Add verbose logging to see processing details:
```python
# In analyze_persona_docs.py, add debug prints
print(f"Processing {len(all_blocks)} text blocks")
print(f"Top similarity scores: {scores[:5]}")
```

## 📋 Requirements Compliance

- ✅ **CPU-only**: No GPU dependencies
- ✅ **Model Size**: < 1GB (80MB actual)
- ✅ **Processing Time**: < 60 seconds for 3-5 documents
- ✅ **Offline Operation**: No internet access required
- ✅ **Generic Solution**: Works for any domain/persona
- ✅ **No Hardcoding**: No file-specific logic
- ✅ **Docker**: Fully containerized solution

## 🎯 Use Cases

This solution is designed for scenarios where users need to quickly find relevant information across multiple documents:

- **Academic Research**: Literature reviews, methodology comparisons
- **Business Analysis**: Market research, competitive analysis
- **Educational Content**: Study guides, exam preparation
- **Professional Training**: Skill development, compliance learning
- **Content Curation**: Personalized reading lists, topic summaries

---

**Ready for production use and hackathon submission!** 🚀 