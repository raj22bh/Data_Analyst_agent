# 🤖 Data Analyst Agent

An AI-powered data analysis tool that automatically processes various file formats and provides intelligent insights using the Llama-4-Maverick model via Together AI.

## link-  https://dataanalystagent-3z3euzvizypsutfikygmeo.streamlit.app/


![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-v1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

 ![Screenshot 2025-06-16 135841](https://github.com/user-attachments/assets/f5bf8dd7-2b61-4953-a3e3-9663bf435319)
 ![Screenshot 2025-06-16 140143](https://github.com/user-attachments/assets/907693ec-0508-4e70-b76d-21ff920045f5)
 
## 🌟 Features

- **Multi-Format File Support**: CSV, Excel, PDF, Word documents, text files, and images
- **AI-Powered Analysis**: Uses Llama-4-Maverick model for intelligent data insights
- **Automatic Visualizations**: Generates correlation heatmaps, distributions, word clouds, and more
- **Interactive Q&A**: Ask natural language questions about your data
- **OCR Capabilities**: Extract and analyze text from images
- **Real-time Processing**: Upload and analyze files instantly

## 📊 Supported File Types

| File Type | Extensions | Analysis Features |
|-----------|------------|-------------------|
| **Spreadsheets** | `.csv`, `.xlsx`, `.xls` | Statistical analysis, correlations, distributions |
| **Documents** | `.txt`, `.docx`, `.pdf` | Text analysis, readability scores, word frequency |
| **Images** | `.png`, `.jpg`, `.jpeg`, `.tiff`, `.bmp` | OCR text extraction and analysis |



## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Together AI API key ([Get yours here](https://www.together.ai/))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/data-analyst-agent.git
   cd data-analyst-agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser** and navigate to `http://localhost:8501`

## 📦 Dependencies

### Core Requirements
```
streamlit>=1.28.0
pandas>=1.5.0
numpy>=1.24.0
matplotlib>=3.6.0
seaborn>=0.12.0
plotly>=5.0.0
together>=0.2.0
```

### Optional Dependencies (Enhanced Features)
```
python-docx>=0.8.11      # Word document processing
PyPDF2>=3.0.0            # PDF processing
Pillow>=9.0.0            # Image processing
pytesseract>=0.3.10      # OCR functionality
wordcloud>=1.9.0         # Word cloud generation
textstat>=0.7.3          # Text readability analysis
scikit-learn>=1.3.0      # Advanced text analysis
```

## 🔧 Configuration

### Getting Your Together AI API Key

1. Visit [Together AI](https://www.together.ai/)
2. Sign up for an account
3. Navigate to the API section
4. Generate your API key
5. Enter the key in the sidebar when running the application

### Rate Limits

The Llama-4-Maverick model has the following limits:
- **0.6 queries per minute** (1 query every ~100 seconds)
- **180M tokens per minute**

For higher limits, contact [Together AI sales](https://www.together.ai/forms/contact-sales).

## 💡 Usage Examples

### 1. Analyzing CSV Data
```python
# Upload a CSV file through the interface
# The agent will automatically:
# - Generate statistical summaries
# - Create correlation heatmaps
# - Show distribution plots
# - Identify patterns and outliers
```

### 2. Document Analysis
```python
# Upload PDF, Word, or text files
# Get insights on:
# - Word frequency analysis
# - Readability scores
# - Content summaries
# - Key topic identification
```

### 3. Image Text Extraction
```python
# Upload images with text
# Features include:
# - OCR text extraction
# - Text analysis of extracted content
# - Word frequency from images
```

## 🎯 Sample Questions

Try asking these questions about your data:

- "What are the key insights from this data?"
- "Can you identify any patterns or trends?"
- "What recommendations would you make based on this analysis?"
- "Are there any outliers or anomalies in the data?"
- "What's the statistical summary of the numeric columns?"

## 🏗️ Project Structure

```
data-analyst-agent/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── requirements-full.txt  # All optional dependencies
├── README.md             # Project documentation
├── examples/            # Sample data files for testing
   ├── sample_data.csv
   ├── sample_document.pdf
   └── sample_image.png

```

## 🛠️ Development

### Setting up Development Environment

1. **Fork the repository**
2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies**
   ```bash
   pip install -r requirements-full.txt
   ```

### Running Tests
```bash
# Run basic functionality tests
python -m pytest tests/

# Run with coverage
python -m pytest --cov=app tests/
```

## 🐛 Troubleshooting

### Common Issues

1. **OCR not working**
   - Install Tesseract: `sudo apt-get install tesseract-ocr` (Linux) or `brew install tesseract` (macOS)
   - Windows: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)

2. **Rate limit errors**
   - Wait 2-3 minutes between queries
   - Consider upgrading your Together AI plan

3. **Memory issues with large files**
   - Process files in smaller chunks
   - Close other applications to free memory

### Getting Help

- 📖 Check the [Documentation](docs/)
- 🐛 Report bugs in [Issues](https://github.com/yourusername/data-analyst-agent/issues)
- 💬 Join discussions in [Discussions](https://github.com/yourusername/data-analyst-agent/discussions)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Ways to Contribute

- 🐛 Report bugs
- 💡 Suggest new features
- 📝 Improve documentation
- 🔧 Submit bug fixes
- ✨ Add new file format support


## 🙏 Acknowledgments

- **Together AI** for providing the Llama-4-Maverick model
- **Streamlit** for the amazing web framework
- **Open Source Community** for the excellent libraries used in this project


## 📈 Roadmap

- [ ] Support for more file formats (JSON, XML, etc.)
- [ ] Database connectivity (SQL, MongoDB)
- [ ] Advanced machine learning models
- [ ] Custom visualization templates
- [ ] Multi-language support
- [ ] API endpoint for programmatic access
- [ ] Docker containerization
- [ ] Cloud deployment options


---

**Made with ❤️ by RJ https://github.com/raj22bh**

If you find this project helpful, please consider giving it a ⭐!
