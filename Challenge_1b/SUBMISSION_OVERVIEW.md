# Challenge 1B Submission Overview
## Persona-Driven Document Intelligence - Adobe India Hackathon 2025

### 🎯 **Solution Overview**
This solution acts as an intelligent document analyst that understands what matters to specific users. Given a collection of PDFs and a persona with a specific job-to-be-done, it extracts and ranks the most relevant sections and insights, making documents speak directly to user needs.

### 🧠 **Technical Approach**
1. **Document Processing**: Extracts text blocks from all PDFs using PyMuPDF, preserving page numbers and document structure
2. **Semantic Understanding**: Uses a lightweight sentence transformer (MiniLM) to convert text into meaningful embeddings
3. **Persona Alignment**: Embeds the user's persona and task description as a query vector
4. **Intelligent Ranking**: Computes semantic similarity between document sections and the persona's needs
5. **Insight Extraction**: Selects the most relevant sections and subsections, ranked by importance
6. **Structured Output**: Generates clean JSON with metadata, ranked sections, and refined text

### 🚀 **Key Features**
- **Persona-Driven**: Understands different user types (researchers, students, professionals)
- **Task-Aware**: Focuses on specific jobs-to-be-done rather than generic content
- **Semantic Intelligence**: Uses advanced NLP to understand meaning, not just keywords
- **Multi-Document**: Processes collections of related documents together
- **Performance Optimized**: Handles 3-5 documents in under 60 seconds
- **Offline Operation**: Works completely offline with no internet dependencies

### 📊 **Performance Metrics**
- **Speed**: < 60 seconds for 3-5 documents
- **Memory**: < 1GB total (including model)
- **Model Size**: 80MB (well under 1GB limit)
- **Accuracy**: High semantic relevance scores on test collections
- **Scalability**: Handles 3-10 documents efficiently

### ✅ **Requirements Compliance**
- ✅ **CPU-only**: No GPU dependencies
- ✅ **Model Size**: < 1GB (80MB actual)
- ✅ **Processing Time**: < 60 seconds for 3-5 documents
- ✅ **Offline Operation**: No internet access required
- ✅ **Generic Solution**: Works for any domain/persona
- ✅ **No Hardcoding**: No file-specific logic
- ✅ **Docker**: Fully containerized solution

### 🔧 **Usage**
```bash
# Build Docker image
docker build --platform linux/amd64 -t persona-pdf-analyzer .

# Run analysis
docker run --rm -v $(pwd)/Collection\ 1/PDFs:/pdfs:ro \
  -v $(pwd)/Collection\ 1/challenge1b_input.json:/input.json:ro \
  -v $(pwd)/Collection\ 1:/outputs \
  persona-pdf-analyzer \
  --input_json /input.json --pdf_dir /pdfs --output_json /outputs/challenge1b_output.json
```

### 📦 **Input/Output Format**

**Input JSON:**
```json
{
  "persona": {"role": "PhD Researcher in Computational Biology"},
  "job_to_be_done": {"task": "Prepare literature review on methodologies"},
  "documents": [{"filename": "doc1.pdf", "title": "Document Title"}]
}
```

**Output JSON:**
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

### 🎯 **Innovation Highlights**
1. **Semantic Understanding**: Uses state-of-the-art sentence transformers for meaning extraction
2. **Persona-Driven Analysis**: Tailors results to specific user needs and tasks
3. **Multi-Document Intelligence**: Processes collections together for comprehensive insights
4. **Intelligent Ranking**: Computes semantic similarity for relevance scoring
5. **Performance Optimization**: Efficient algorithms that meet strict time and memory constraints

### 📋 **Files Included**
- `analyze_persona_docs.py`: Semantic analysis script with sentence transformers
- `Dockerfile`: CPU-only, AMD64 compatible container
- `requirements.txt`: Dependencies including sentence-transformers
- `README.md`: Complete documentation with examples

### 🏆 **Ready for Production**
This solution is production-ready with comprehensive error handling, clear documentation, and optimized performance. It demonstrates advanced NLP capabilities while meeting all hackathon constraints and providing genuine value to users.

### 🎯 **Use Cases**
- **Academic Research**: Literature reviews, methodology comparisons
- **Business Analysis**: Market research, competitive analysis
- **Educational Content**: Study guides, exam preparation
- **Professional Training**: Skill development, compliance learning
- **Content Curation**: Personalized reading lists, topic summaries

---
*Submitted for Adobe India Hackathon 2025 - Challenge 1B* 