"""
Example usage of PaperSummarizer
"""

from paper_summarizer import PaperSummarizer
import json

def example_pdf_analysis():
    """Example: Analyze a PDF file"""
    summarizer = PaperSummarizer()
    
    # Analyze PDF with metadata
    result = summarizer.summarize_paper(
        input_source="path/to/paper.pdf",
        input_type="pdf",
        metadata={
            "title": "Attention Is All You Need",
            "authors": "Vaswani et al.",
            "venue_year": "NIPS 2017",
            "doi_or_arxiv": "arXiv:1706.03762"
        }
    )
    
    print("Markdown Summary:")
    print(result['markdown'])
    print("\nJSON Data:")
    print(json.dumps(result['json'], indent=2))

def example_arxiv_analysis():
    """Example: Analyze paper from ArXiv URL"""
    summarizer = PaperSummarizer()
    
    # Analyze ArXiv paper
    result = summarizer.summarize_paper(
        input_source="https://arxiv.org/abs/1706.03762",
        input_type="url"
    )
    
    print("Analysis complete!")
    print(f"Title: {result['json']['title']}")
    print(f"TL;DR: {result['json']['tldr']}")

def example_text_analysis():
    """Example: Analyze raw text"""
    summarizer = PaperSummarizer()
    
    paper_text = """
    Abstract
    
    The dominant sequence transduction models are based on complex recurrent or 
    convolutional neural networks that include an encoder and a decoder. The best 
    performing models also connect the encoder and decoder through an attention 
    mechanism. We propose a new simple network architecture, the Transformer, 
    based solely on attention mechanisms, dispensing with recurrence and 
    convolutions entirely.
    
    1. Introduction
    
    Recurrent neural networks, long short-term memory and gated recurrent neural 
    networks in particular, have been firmly established as state of the art 
    approaches in sequence modeling and transduction problems such as language 
    modeling and machine translation.
    
    2. Model Architecture
    
    The Transformer follows this overall architecture using stacked self-attention 
    and point-wise, fully connected layers for both the encoder and decoder, 
    shown in the left and right halves of Figure 1, respectively.
    """
    
    result = summarizer.summarize_paper(
        input_source=paper_text,
        input_type="text",
        metadata={
            "title": "Attention Is All You Need",
            "authors": "Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz Kaiser, Illia Polosukhin"
        }
    )
    
    print("Text Analysis Results:")
    print(f"Contributions: {result['json']['contributions']}")
    print(f"Method: {result['json']['method']['summary']}")

if __name__ == "__main__":
    print("PaperSummarizer Examples")
    print("=" * 50)
    
    # Run examples (uncomment to test)
    # example_pdf_analysis()
    # example_arxiv_analysis()
    example_text_analysis()
