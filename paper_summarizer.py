import re
import json
import requests
from typing import Dict, List, Any, Optional, Tuple
import PyPDF2
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import spacy
from transformers import pipeline
import arxiv
import io
import time
import tempfile
import os


class PaperSummarizer:
    """
    Academically rigorous assistant for producing faithful research paper summaries.
    """
    
    def __init__(self):
        """Initialize the PaperSummarizer with required models and tools."""
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("Warning: spaCy model not found. Install with: python -m spacy download en_core_web_sm")
            self.nlp = None
        
        # Download required NLTK data
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text content from a PDF file."""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text.strip()
        except Exception as e:
            raise ValueError(f"Error reading PDF: {str(e)}")
    
    def fetch_paper_from_url(self, url: str) -> Tuple[str, Dict[str, str]]:
        """Fetch paper content from URL (ArXiv, etc.)."""
        metadata = {}
        
        # Handle ArXiv URLs
        if "arxiv.org" in url:
            arxiv_id = self._extract_arxiv_id(url)
            if arxiv_id:
                return self._fetch_from_arxiv(arxiv_id)
        
        # Handle general URLs
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            if response.headers.get('content-type', '').startswith('application/pdf'):
                # Handle PDF URLs
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(response.content))
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text.strip(), metadata
            else:
                # Handle HTML pages
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract metadata
                title_tag = soup.find('title')
                if title_tag:
                    metadata['title'] = title_tag.get_text().strip()
                
                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.decompose()
                
                text = soup.get_text()
                return self._clean_text(text), metadata
                
        except Exception as e:
            raise ValueError(f"Error fetching URL: {str(e)}")
    
    def _extract_arxiv_id(self, url: str) -> Optional[str]:
        """Extract ArXiv ID from URL."""
        patterns = [
            r'arxiv\.org/abs/([0-9]+\.[0-9]+)',
            r'arxiv\.org/pdf/([0-9]+\.[0-9]+)',
            r'([0-9]+\.[0-9]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    def _fetch_from_arxiv(self, arxiv_id: str) -> Tuple[str, Dict[str, str]]:
        """Fetch paper from ArXiv API with retry logic."""
        max_retries = 3
        retry_delay = 1
        
        for attempt in range(max_retries):
            try:
                # Use arxiv library's built-in search
                search = arxiv.Search(id_list=[arxiv_id])
                paper = next(search.results())
                
                metadata = {
                    'title': paper.title,
                    'authors': ', '.join([author.name for author in paper.authors]),
                    'venue_year': f"ArXiv {paper.published.year}",
                    'doi_or_arxiv': f"arXiv:{arxiv_id}",
                    'abstract': paper.summary
                }
                
                # Try using arxiv library's download method first
                try:
                    with tempfile.TemporaryDirectory() as temp_dir:
                        paper.download_pdf(dirpath=temp_dir, filename=f"{arxiv_id}.pdf")
                        pdf_path = os.path.join(temp_dir, f"{arxiv_id}.pdf")
                        
                        # Extract text from downloaded PDF
                        with open(pdf_path, 'rb') as file:
                            pdf_reader = PyPDF2.PdfReader(file)
                            text = ""
                            for page in pdf_reader.pages:
                                text += page.extract_text() + "\n"
                        
                        return text.strip(), metadata
                        
                except Exception as download_error:
                    # Fallback to manual PDF download with retry
                    print(f"ArXiv download failed, trying manual download (attempt {attempt + 1}): {download_error}")
                    
                    pdf_url = paper.pdf_url
                    if pdf_url.startswith('http://'):
                        pdf_url = pdf_url.replace('http://', 'https://')
                    
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                    }
                    
                    response = requests.get(pdf_url, headers=headers, timeout=60)
                    response.raise_for_status()
                    pdf_reader = PyPDF2.PdfReader(io.BytesIO(response.content))
                    
                    text = ""
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
                    
                    return text.strip(), metadata
                    
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"ArXiv fetch attempt {attempt + 1} failed: {str(e)}")
                    time.sleep(retry_delay * (2 ** attempt))  # Exponential backoff
                    continue
                else:
                    # Try alternative approach - use abstract if PDF fails
                    try:
                        search = arxiv.Search(id_list=[arxiv_id])
                        paper = next(search.results())
                        
                        metadata = {
                            'title': paper.title,
                            'authors': ', '.join([author.name for author in paper.authors]),
                            'venue_year': f"ArXiv {paper.published.year}",
                            'doi_or_arxiv': f"arXiv:{arxiv_id}",
                            'abstract': paper.summary
                        }
                        
                        # Return abstract as fallback text
                        fallback_text = f"Title: {paper.title}\n\nAbstract: {paper.summary}\n\nNote: Full PDF text could not be retrieved due to connection issues."
                        return fallback_text, metadata
                        
                    except Exception:
                        raise ValueError(f"Error fetching ArXiv paper after {max_retries} attempts: {str(e)}")
        
        raise ValueError(f"Failed to fetch ArXiv paper after {max_retries} attempts")
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text content."""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove non-printable characters except newlines
        text = re.sub(r'[^\x20-\x7E\n]', '', text)
        return text.strip()
    
    def _extract_sections(self, text: str) -> Dict[str, str]:
        """Extract paper sections using pattern matching."""
        sections = {}
        
        # Common section patterns
        section_patterns = {
            'abstract': r'(?i)abstract\s*\n(.*?)(?=\n\s*(?:introduction|1\.|keywords|index terms))',
            'introduction': r'(?i)(?:1\.\s*)?introduction\s*\n(.*?)(?=\n\s*(?:2\.|related work|background|method))',
            'method': r'(?i)(?:method|approach|algorithm|architecture)\s*\n(.*?)(?=\n\s*(?:\d+\.|experiment|evaluation|result))',
            'results': r'(?i)(?:result|experiment|evaluation)\s*\n(.*?)(?=\n\s*(?:\d+\.|discussion|conclusion|limitation))',
            'conclusion': r'(?i)conclusion\s*\n(.*?)(?=\n\s*(?:reference|acknowledgment|appendix))',
            'limitations': r'(?i)limitation\s*\n(.*?)(?=\n\s*(?:reference|acknowledgment|appendix))'
        }
        
        for section_name, pattern in section_patterns.items():
            match = re.search(pattern, text, re.DOTALL)
            if match:
                sections[section_name] = match.group(1).strip()
        
        # If no sections found, use the full text
        if not sections:
            sections['full_text'] = text
        
        return sections
    
    def _extract_citations(self, text: str) -> List[str]:
        """Extract citation markers from text."""
        # Pattern for various citation formats
        citation_patterns = [
            r'\[(\d+(?:,\s*\d+)*)\]',  # [1], [1,2,3]
            r'\(([A-Za-z]+(?:\s+et\s+al\.?)?,?\s+\d{4})\)',  # (Smith et al., 2022)
            r'\(([A-Za-z]+,?\s+\d{4})\)'  # (Smith, 2022)
        ]
        
        citations = set()
        for pattern in citation_patterns:
            matches = re.findall(pattern, text)
            citations.update(matches)
        
        return sorted(list(citations))
    
    def _extract_equations(self, text: str) -> List[str]:
        """Extract LaTeX equations from text."""
        # Pattern for LaTeX equations
        equation_patterns = [
            r'\$\$(.*?)\$\$',  # Display math
            r'\$(.*?)\$',      # Inline math
            r'\\begin\{equation\}(.*?)\\end\{equation\}',  # Equation environment
            r'\\begin\{align\}(.*?)\\end\{align\}'         # Align environment
        ]
        
        equations = []
        for pattern in equation_patterns:
            matches = re.findall(pattern, text, re.DOTALL)
            equations.extend([eq.strip() for eq in matches if eq.strip()])
        
        return equations
    
    def _extract_metrics_and_results(self, text: str) -> List[Dict[str, Any]]:
        """Extract numerical results and metrics from text."""
        results = []
        
        # Pattern for common metrics (accuracy, F1, BLEU, etc.)
        metric_patterns = [
            r'(accuracy|f1|bleu|rouge|perplexity|loss)\s*[:=]\s*([\d.]+)%?',
            r'([\d.]+)%?\s*(accuracy|f1|bleu|rouge)',
            r'achieves?\s+([\d.]+)%?\s+(accuracy|f1|bleu|rouge)',
            r'(state-of-the-art|sota|best)\s+.*?([\d.]+)%?'
        ]
        
        for pattern in metric_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if len(match) == 2:
                    metric, value = match
                    results.append({
                        'metric': metric.lower(),
                        'value': value,
                        'dataset_or_benchmark': 'Not specified',
                        'compared_to': 'Not specified',
                        'evidence_citation': 'Not specified'
                    })
        
        return results
    
    def summarize_paper(self, input_source: str, input_type: str = 'auto', 
                       metadata: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Main method to summarize a research paper.
        
        Args:
            input_source: Path to PDF, URL, or raw text
            input_type: 'pdf', 'url', 'text', or 'auto'
            metadata: Optional metadata dict
        
        Returns:
            Dict containing markdown summary and JSON object
        """
        
        # Determine input type and extract text
        if input_type == 'auto':
            if input_source.startswith(('http://', 'https://')):
                input_type = 'url'
            elif input_source.endswith('.pdf'):
                input_type = 'pdf'
            else:
                input_type = 'text'
        
        # Extract text and metadata
        if input_type == 'pdf':
            text = self.extract_text_from_pdf(input_source)
            paper_metadata = metadata or {}
        elif input_type == 'url':
            text, paper_metadata = self.fetch_paper_from_url(input_source)
            if metadata:
                paper_metadata.update(metadata)
        else:  # text
            text = input_source
            paper_metadata = metadata or {}
        
        # Process the paper
        return self._process_paper_text(text, paper_metadata)
    
    def _process_paper_text(self, text: str, metadata: Dict[str, str]) -> Dict[str, Any]:
        """Process paper text and generate summary."""
        
        # Extract paper components
        sections = self._extract_sections(text)
        citations = self._extract_citations(text)
        equations = self._extract_equations(text)
        results = self._extract_metrics_and_results(text)
        
        # Generate summary components
        summary_data = self._generate_summary_components(text, sections, metadata)
        
        # Create JSON object
        json_output = {
            "title": metadata.get('title', 'Not specified'),
            "tldr": summary_data['tldr'],
            "contributions": summary_data['contributions'],
            "method": {
                "summary": summary_data['method_summary'],
                "equations": equations[:5]  # Limit to first 5 equations
            },
            "datasets": summary_data['datasets'],
            "setup": {
                "baselines": summary_data['baselines'],
                "compute": summary_data['compute'],
                "code_or_data_links": summary_data['links']
            },
            "results": results[:10],  # Limit to first 10 results
            "ablations": summary_data['ablations'],
            "limitations": summary_data['limitations'],
            "risks_or_ethics": summary_data['risks'],
            "glossary": summary_data['glossary'],
            "citations_used": citations[:20]  # Limit to first 20 citations
        }
        
        # Generate Markdown
        markdown_output = self._generate_markdown(summary_data, json_output, metadata)
        
        return {
            'markdown': markdown_output,
            'json': json_output,
            'metadata': metadata
        }
    
    def _generate_summary_components(self, text: str, sections: Dict[str, str], 
                                   metadata: Dict[str, str]) -> Dict[str, Any]:
        """Generate summary components from paper text."""
        
        # Use abstract or first part of text for TL;DR
        abstract_text = sections.get('abstract', text[:1000])
        sentences = sent_tokenize(abstract_text)
        tldr = ' '.join(sentences[:3]) if len(sentences) >= 3 else abstract_text[:300]
        
        # Extract contributions (look for numbered lists, bullet points)
        contributions = self._extract_contributions(text)
        
        # Extract method summary
        method_text = sections.get('method', sections.get('full_text', text))
        method_summary = self._extract_method_summary(method_text)
        
        # Extract other components
        datasets = self._extract_datasets(text)
        baselines = self._extract_baselines(text)
        limitations = self._extract_limitations(text)
        glossary = self._extract_glossary(text)
        
        return {
            'tldr': tldr,
            'contributions': contributions,
            'method_summary': method_summary,
            'datasets': datasets,
            'baselines': baselines,
            'compute': 'Not specified',
            'links': [],
            'ablations': [],
            'limitations': limitations,
            'risks': [],
            'glossary': glossary
        }
    
    def _extract_contributions(self, text: str) -> List[str]:
        """Extract paper contributions."""
        contributions = []
        
        # Look for contribution sections
        contrib_patterns = [
            r'(?i)contributions?:?\s*\n(.*?)(?=\n\s*\d+\.|\n\s*[A-Z])',
            r'(?i)our contributions?.*?:?\s*(.*?)(?=\n\s*\d+\.|\n\s*[A-Z])',
            r'(?i)we (?:propose|present|introduce|contribute)\s+(.*?)(?=\.|\n)'
        ]
        
        for pattern in contrib_patterns:
            matches = re.findall(pattern, text, re.DOTALL)
            for match in matches:
                # Split by bullet points or numbers
                items = re.split(r'[•\-\*]\s*|\d+\)\s*|\d+\.\s*', match)
                contributions.extend([item.strip() for item in items if item.strip()])
        
        return contributions[:5] if contributions else ['Not specified']
    
    def _extract_method_summary(self, text: str) -> str:
        """Extract method summary."""
        # Look for method description
        method_sentences = sent_tokenize(text[:2000])  # First 2000 chars
        return ' '.join(method_sentences[:3]) if method_sentences else 'Not specified'
    
    def _extract_datasets(self, text: str) -> List[str]:
        """Extract dataset names."""
        # Common dataset patterns
        dataset_patterns = [
            r'(?i)(imagenet|cifar|mnist|coco|squad|glue|superglue|wmt|opus)',
            r'(?i)dataset[s]?\s*[:=]\s*([A-Za-z0-9\-_]+)',
            r'(?i)we (?:use|evaluate on|test on)\s+([A-Za-z0-9\-_]+)\s+dataset'
        ]
        
        datasets = set()
        for pattern in dataset_patterns:
            matches = re.findall(pattern, text)
            datasets.update(matches)
        
        return list(datasets) if datasets else ['Not specified']
    
    def _extract_baselines(self, text: str) -> List[str]:
        """Extract baseline methods."""
        baseline_patterns = [
            r'(?i)baseline[s]?\s*[:=]\s*([A-Za-z0-9\-_\s]+)',
            r'(?i)we compare (?:with|against|to)\s+([A-Za-z0-9\-_\s]+)',
            r'(?i)compared to\s+([A-Za-z0-9\-_\s]+)'
        ]
        
        baselines = set()
        for pattern in baseline_patterns:
            matches = re.findall(pattern, text)
            baselines.update([b.strip() for b in matches])
        
        return list(baselines) if baselines else ['Not specified']
    
    def _extract_limitations(self, text: str) -> List[str]:
        """Extract limitations."""
        limitation_patterns = [
            r'(?i)limitations?:?\s*\n(.*?)(?=\n\s*\d+\.|\n\s*[A-Z])',
            r'(?i)(?:however|but|limitation|drawback|weakness).*?([^.]+\.)',
        ]
        
        limitations = []
        for pattern in limitation_patterns:
            matches = re.findall(pattern, text, re.DOTALL)
            limitations.extend([lim.strip() for lim in matches if lim.strip()])
        
        return limitations[:3] if limitations else ['Not specified']
    
    def _extract_glossary(self, text: str) -> List[Dict[str, str]]:
        """Extract key terms and definitions."""
        # Simple glossary extraction - look for definitions
        definition_patterns = [
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+is\s+(?:a|an)\s+([^.]+\.)',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*[:=]\s*([^.]+\.)',
        ]
        
        glossary = []
        for pattern in definition_patterns:
            matches = re.findall(pattern, text)
            for term, definition in matches:
                if len(glossary) < 10:  # Limit to 10 terms
                    glossary.append({
                        'term': term.strip(),
                        'definition': definition.strip()
                    })
        
        return glossary if glossary else [{'term': 'Not specified', 'definition': 'Not specified'}]
    
    def _generate_markdown(self, summary_data: Dict[str, Any], 
                          json_data: Dict[str, Any], 
                          metadata: Dict[str, str]) -> str:
        """Generate Markdown summary following the structured template format."""
        
        # Format DOI/ArXiv as a link if it's an ArXiv paper
        doi_arxiv = metadata.get('doi_or_arxiv', 'Not specified')
        if doi_arxiv.startswith('arXiv:'):
            arxiv_id = doi_arxiv.replace('arXiv:', '')
            doi_link = f"[{doi_arxiv}](https://arxiv.org/abs/{arxiv_id})"
        else:
            doi_link = doi_arxiv
        
        markdown = f"""# 📄 Research Paper Summary: {json_data['title']}

**Authors:** {metadata.get('authors', 'Not specified')}  
**Venue/Year:** {metadata.get('venue_year', 'Not specified')}  
**DOI:** {doi_link}

---

## 🧠 TL;DR
> {json_data['tldr']}

---

## 🚀 Why It Matters
This research contributes to the field by addressing key challenges and proposing novel solutions with practical implications.

---

## 🔍 Core Contributions"""
        
        for contrib in json_data['contributions']:
            if contrib != 'Not specified':
                markdown += f"\n- {contrib}"
        
        if not any(contrib != 'Not specified' for contrib in json_data['contributions']):
            markdown += "\n- Core contributions not clearly specified in the paper"
        
        markdown += f"""

---

## 🧪 Method
{json_data['method']['summary']}"""
        
        if json_data['method']['equations']:
            markdown += "\n\n**Key components:**"
            for eq in json_data['method']['equations'][:3]:  # Limit to 3 equations
                markdown += f"\n  - {eq}"
        
        markdown += f"""

---

## 📊 Data & Setup
- **Datasets:** {', '.join(json_data['datasets'])}
- **Compute:** {json_data['setup']['compute']}
- **Baselines:** {', '.join(json_data['setup']['baselines'])}

---

## 📈 Results"""
        
        if json_data['results']:
            markdown += "\n| Task | Score | Notes |\n|------|-------|-------|\n"
            for result in json_data['results'][:5]:  # Limit to 5 results
                markdown += f"| {result['metric'].title()} | {result['value']} | {result['dataset_or_benchmark']} |\n"
        else:
            markdown += "\n- Specific numerical results not clearly extracted from the paper"
        
        markdown += f"""

---

## ⚠️ Limitations & Risks"""
        
        for limitation in json_data['limitations']:
            if limitation != 'Not specified':
                markdown += f"\n- {limitation}"
        
        if not any(lim != 'Not specified' for lim in json_data['limitations']):
            markdown += "\n- Limitations not clearly specified in the paper"
        
        markdown += f"""

---

## 🔁 Reproducibility"""
        
        if json_data['setup']['code_or_data_links']:
            markdown += f"\n- **Code:** {', '.join(json_data['setup']['code_or_data_links'])}"
        else:
            markdown += "\n- **Code:** Not specified"
        
        # Add model sizes if available in metadata
        if 'model_sizes' in metadata:
            markdown += f"\n- **Model Sizes:** {metadata['model_sizes']}"
        
        markdown += f"""

---

## 📚 Glossary"""
        
        for term_def in json_data['glossary'][:5]:  # Limit to 5 terms
            if term_def['term'] != 'Not specified':
                markdown += f"\n- **{term_def['term']}:** {term_def['definition']}"
        
        if not any(term['term'] != 'Not specified' for term in json_data['glossary']):
            markdown += "\n- Key terms not clearly extracted from the paper"
        
        markdown += f"""

---

## 🔗 Citations Used
{', '.join(json_data['citations_used'][:12]) if json_data['citations_used'] else 'Citations not clearly extracted'}

---

*Generated using automated paper summarization. Feel free to modify this summary as needed.*
"""
        
        return markdown
