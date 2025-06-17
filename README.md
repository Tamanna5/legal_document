# Legal Document Analysis and Summarization System

This project implements an AI-driven system for analyzing and summarizing legal documents using advanced NLP techniques. The system provides a web interface for uploading documents and generates concise, professional summaries in both PDF and JSON formats.

## Features

- **Web Interface**: Modern, user-friendly interface for document upload and analysis
- **Document Processing**: Supports PDF, DOCX, and TXT formats
- **Smart Summarization**: Generates concise 1-2 page summaries
- **Key Information Extraction**:
  - Legal entities identification
  - Key clauses extraction
  - Obligations and rights analysis
  - Section-by-section summaries
- **Multiple Output Formats**:
  - PDF summary with professional formatting
  - JSON format for data processing
- **File Management**: Automatic organization of uploaded files and summaries

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd legal_document
```

2. Create and activate a virtual environment:
```bash
python -m venv legal_nlp_env
source legal_nlp_env/bin/activate  # On Windows: legal_nlp_env\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Download the required SpaCy model:
```bash
python -m spacy download en_core_web_lg
```

5. Download NLTK data:
```python
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

## Usage

1. Start the web application:
```bash
python main.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. Upload a legal document:
   - Drag and drop a file or click to select
   - Supported formats: PDF, DOCX, TXT
   - Maximum file size: 10MB

4. View and download results:
   - Analysis results are displayed in the web interface
   - Download PDF summary
   - Download JSON data

## Project Structure

```
legal_document/
├── main.py              # Application entry point
├── web_app.py          # Flask web application
├── document_processor.py  # Document loading and preprocessing
├── entity_extractor.py    # Entity recognition and information extraction
├── summarizer.py         # Document summarization
├── legal_analyzer.py     # Main analysis logic
├── pdf_generator.py      # PDF summary generation
├── templates/           # HTML templates
│   └── index.html      # Main web interface
├── uploads/            # Uploaded files and generated summaries
├── requirements.txt    # Project dependencies
└── README.md          # This file
```

## Dependencies

- Flask: Web framework
- spacy: Natural language processing
- nltk: Text processing and tokenization
- transformers: Text summarization (indirectly via SpaCy/other NLP models)
- torch: Deep learning framework (dependency for transformers)
- pdfplumber: PDF text extraction
- python-docx: DOCX file handling
- reportlab: PDF generation
- werkzeug: Web server utilities

## Features in Detail

### Document Analysis
- Extracts key legal entities and terms
- Identifies important clauses and their context
- Analyzes obligations and rights
- Generates section-by-section summaries

### Summary Generation
- Creates concise 1-2 page summaries
- Professional PDF formatting
- Structured JSON output
- Smart section selection for optimal coverage

### Web Interface
- Modern, responsive design
- Drag-and-drop file upload
- Real-time analysis status
- Easy download of results

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 