# 📄 Research Paper Summarizer

An academically rigorous AI assistant for producing faithful, structured research paper summaries. Transforms complex academic papers into beautifully formatted, emoji-rich summaries that follow a consistent template structure.

## ✨ Features

- **🎯 Faithful Summarization**: Only uses information present in the provided text
- **📁 Multiple Input Formats**: PDF files, text input, URLs, ArXiv papers
- **📊 Dual Output**: Human-readable Markdown + structured JSON
- **📚 Citation Preservation**: Maintains in-text citation markers
- **🔬 Academic Rigor**: Preserves equations, terminology, and technical details
- **🌐 Web Interface**: Easy-to-use Flask web application
- **📋 Structured Template**: Consistent format with emojis and clear sections

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/paper-summarizer.git
cd paper-summarizer

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm
```

### Web Interface
```bash
python app.py
```
Navigate to `http://localhost:5000`

### Command Line Usage
```python
from paper_summarizer import PaperSummarizer

# Initialize summarizer
summarizer = PaperSummarizer()

# Summarize from different sources
result = summarizer.summarize_paper("path/to/paper.pdf")  # PDF file
result = summarizer.summarize_paper("https://arxiv.org/abs/1706.03762")  # ArXiv URL
result = summarizer.summarize_paper("paper text here", input_type='text')  # Raw text

# Access outputs
print(result['markdown'])  # Formatted summary
print(result['json'])      # Structured data
```

## 📋 Output Format

The tool produces beautifully structured summaries following this template:

### 📄 Markdown Summary
```markdown
# 📄 Research Paper Summary: [Title]

**Authors:** [Author List]
**Venue/Year:** [Publication Info]
**DOI:** [DOI/ArXiv Link]

---

## 🧠 TL;DR
> [Concise summary of the paper]

---

## 🚀 Why It Matters
[Significance and impact]

---

## 🔍 Core Contributions
- [Key contribution 1]
- [Key contribution 2]

---

## 🧪 Method
[Technical approach and methodology]

---

## 📊 Data & Setup
- **Datasets:** [Dataset names]
- **Compute:** [Hardware/training info]
- **Baselines:** [Comparison methods]

---

## 📈 Results
| Task | Score | Notes |
|------|-------|-------|
| [Metric] | [Value] | [Context] |

---

## ⚠️ Limitations & Risks
- [Limitation 1]
- [Limitation 2]

---

## 🔁 Reproducibility
- **Code:** [Repository links]
- **Model Sizes:** [Parameter counts]

---

## 📚 Glossary
- **[Term]:** [Definition]

---

## 🔗 Citations Used
[Citation markers from paper]
```

### 🔧 JSON Structure
```json
{
  "title": "Paper Title",
  "tldr": "Brief summary",
  "contributions": ["List of contributions"],
  "method": {
    "summary": "Method description",
    "equations": ["Key equations"]
  },
  "datasets": ["Dataset names"],
  "results": [{"metric": "accuracy", "value": "95.2%"}],
  "limitations": ["Identified limitations"],
  "glossary": [{"term": "Term", "definition": "Definition"}]
}
```

## 🌐 API Endpoints

- `POST /summarize` - Upload and summarize a paper file
- `POST /summarize_url` - Summarize paper from URL (ArXiv, etc.)
- `POST /summarize_text` - Summarize from raw text input

## 📁 Project Structure

```
paper-summarizer/
├── 📄 README.md              # This file
├── 📋 requirements.txt       # Python dependencies
├── 🐍 paper_summarizer.py    # Core summarization logic
├── 🌐 app.py                 # Flask web application
├── 🖥️ cli.py                 # Command-line interface
├── ⚙️ config.py              # Configuration settings
├── 🏃 run.py                 # Application runner
├── 📝 sample_research_summary.md  # Template example
├── 🧪 test_summarizer.py     # Unit tests
├── 📁 templates/             # HTML templates
├── 📁 static/                # CSS/JS assets
└── 📁 examples/              # Usage examples
```

## 🔒 Academic Standards

The summarizer follows strict academic principles:

1. **🎯 Faithfulness**: Only information from source text
2. **📚 Citations**: Preserves in-text citation markers
3. **💬 Quotes**: Verbatim text in double quotes
4. **🧮 Equations**: Exact LaTeX reproduction
5. **📖 Terminology**: Uses paper's original vocabulary
6. **❓ Uncertainty**: States confidence levels when unsure

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with modern NLP libraries (spaCy, NLTK, Transformers)
- Inspired by academic paper summarization best practices
- Template design optimized for readability and consistency


This is Ahmed