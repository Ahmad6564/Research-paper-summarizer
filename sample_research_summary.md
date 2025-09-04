
# 📄 Research Paper Summary: Attention Is All You Need

**Authors:** Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, Illia Polosukhin  
**Venue/Year:** arXiv, 2017  
**DOI:** [arXiv:1706.03762](https://arxiv.org/abs/1706.03762)

---

## 🧠 TL;DR
> Introduced the Transformer architecture, replacing recurrence with self-attention, achieving state-of-the-art results in machine translation.

---

## 🚀 Why It Matters
This paper laid the foundation for modern NLP models like BERT, GPT, and T5 by demonstrating that attention mechanisms alone can outperform RNNs and CNNs in sequence modeling tasks.

---

## 🔍 Core Contributions
- Proposed the **Transformer** architecture based solely on attention.
- Introduced **multi-head attention** and **positional encoding**.
- Achieved superior performance on translation benchmarks with reduced training time.

---

## 🧪 Method
- Encoder-decoder structure with 6 stacked layers each.
- Key components:
  - Scaled Dot-Product Attention
  - Multi-Head Attention
  - Position-wise Feed-Forward Networks
  - Positional Encoding

---

## 📊 Data & Setup
- **Datasets:** WMT 2014 English-German, English-French
- **Compute:** 8 NVIDIA P100 GPUs, 3.5 days training
- **Baselines:** RNN/CNN-based seq2seq models

---

## 📈 Results
| Task | BLEU Score | Notes |
|------|------------|-------|
| En→De | 28.4 | State-of-the-art |
| En→Fr | 41.8 | State-of-the-art |

---

## ⚠️ Limitations & Risks
- Requires large datasets and compute resources
- Lacks inductive bias for sequential locality

---

## 🔁 Reproducibility
- **Code:** [Tensor2Tensor](https://github.com/tensorflow/tensor2tensor)
- **Model Sizes:** Base (65M params), Big (213M params)

---

## 📚 Glossary
- **Self-Attention:** Computes relationships between all tokens in a sequence
- **Multi-Head Attention:** Parallel attention layers capturing diverse features
- **Positional Encoding:** Adds order information to token embeddings

---

## 🔗 Citations Used
[1], [2], [5], [10], [11], [12], [13], [14], [15], [16], [17], [18]

---

*Feel free to modify this template for your own research paper summaries.*
