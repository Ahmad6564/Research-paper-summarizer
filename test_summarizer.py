"""
Test script for PaperSummarizer
"""

import json
from paper_summarizer import PaperSummarizer

def test_text_summarization():
    """Test basic text summarization functionality"""
    
    # Sample research paper text
    sample_text = """
    Abstract
    
    We present a novel approach to natural language processing using transformer 
    architectures. Our method achieves state-of-the-art results on multiple 
    benchmarks including GLUE and SuperGLUE. The key innovation is a new 
    attention mechanism that reduces computational complexity from O(n²) to O(n log n).
    
    1. Introduction
    
    Natural language processing has seen remarkable progress with the introduction 
    of transformer models [1]. However, these models suffer from quadratic 
    complexity in sequence length, limiting their applicability to long documents.
    
    2. Method
    
    Our approach introduces sparse attention patterns that maintain model 
    performance while reducing computational requirements. The core equation is:
    
    Attention(Q,K,V) = softmax(QK^T/√d_k)V
    
    We modify this to use only the top-k attention weights, resulting in:
    
    SparseAttention(Q,K,V) = softmax(TopK(QK^T/√d_k))V
    
    3. Experiments
    
    We evaluate our method on GLUE benchmark achieving 89.2% average score, 
    compared to BERT's 84.6%. On SuperGLUE, we achieve 71.8% vs BERT's 69.0%.
    
    4. Results
    
    Our sparse transformer achieves:
    - GLUE: 89.2% (vs BERT 84.6%)
    - SuperGLUE: 71.8% (vs BERT 69.0%)
    - Inference speed: 3.2x faster than BERT
    - Memory usage: 40% reduction
    
    5. Limitations
    
    The method may lose some long-range dependencies due to sparse attention.
    Performance on very long sequences (>2048 tokens) needs further evaluation.
    
    References
    [1] Vaswani et al. Attention is All You Need. NIPS 2017.
    """
    
    print("Testing PaperSummarizer with sample text...")
    
    try:
        summarizer = PaperSummarizer()
        
        metadata = {
            'title': 'Sparse Attention for Efficient Transformers',
            'authors': 'John Doe, Jane Smith',
            'venue_year': 'ICML 2023',
            'doi_or_arxiv': 'arXiv:2301.12345'
        }
        
        result = summarizer.summarize_paper(sample_text, 'text', metadata)
        
        print("✅ Summarization successful!")
        print(f"Title: {result['json']['title']}")
        print(f"TL;DR: {result['json']['tldr']}")
        print(f"Contributions: {len(result['json']['contributions'])}")
        print(f"Results found: {len(result['json']['results'])}")
        
        # Save test output
        with open('test_output.md', 'w', encoding='utf-8') as f:
            f.write(result['markdown'])
        
        with open('test_output.json', 'w', encoding='utf-8') as f:
            json.dump(result['json'], f, indent=2)
        
        print("✅ Test outputs saved to test_output.md and test_output.json")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_text_summarization()
    if success:
        print("\n🎉 PaperSummarizer is working correctly!")
    else:
        print("\n💥 PaperSummarizer test failed!")
