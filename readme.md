# RAG Policy Question-Answering Assistant

A lightweight **Retrieval-Augmented Generation (RAG)** system built to answer
company policy questions accurately while **avoiding hallucinations**.
This project focuses on **prompt engineering, retrieval quality, evaluation,
and reasoning**, rather than UI or large-scale infrastructure.

---

## 🎯 Objective

The goal of this project is to demonstrate:
- Prompt engineering for grounded responses
- Hallucination prevention
- Evaluation and reasoning


---

## 🏗️ Project Structure

```

rag-policy-qa/
│
├── data/
│   ├── refund_policy.txt
│   ├── cancellation_policy.txt
│   ├── shipping_policy.txt
│   └── warranty_policy.txt
│
├── src/
│   ├── rag.py          # Core RAG pipeline
│   └── prompts.py     # Prompt versions (V1, V2)
│
├── evaluation/
│   ├── evaluation.py  # Manual evaluation script
│   └── results.md     # Final evaluation results
│
├── main.py            # Interactive CLI for Q&A
├── requirements.txt
└── README.md

````

---

## ⚙️ Architecture Overview

1. **Document Loading**
   - Policy documents are loaded from the `data/` directory
   - Each document is tagged with metadata (`source: filename`)

2. **Chunking**
   - Documents are split using `RecursiveCharacterTextSplitter`
   - Chunk size: 500 characters
   - Overlap: 50 characters
   - This balances semantic completeness with retrieval precision

3. **Embeddings**
   - Local embeddings using `sentence-transformers/all-MiniLM-L6-v2`
   - Chosen to avoid API quota limits and ensure deterministic behavior

4. **Vector Store**
   - ChromaDB is used for semantic similarity search
   - Top-k retrieval with similarity scores

5. **LLM Generation**
   - Gemini (`gemini-2.x-flash`) is used for answer generation
   - The model is strictly instructed to answer **only from retrieved context**

6. **Safety & Controls**
   - Retrieval score thresholds prevent low-quality context usage
   - Out-of-scope queries are explicitly declined
   - Confidence levels are returned with each answer

---

## 🧠 Prompt Engineering

### Prompt V1 (Baseline)
- Simple instruction to answer using provided context
- No hallucination prevention
- No structured output

### Prompt V2 (Improved – Used in Final System)
Improvements:
- Explicit instruction to use **only retrieved context**
- Clear handling of missing or unrelated questions
- Structured JSON output
- Confidence calibration (`high | medium | low`)
- Mandatory source citation

Prompt iteration significantly improved grounding and safety.

---

## 📊 Evaluation

The system was evaluated using 8 manually designed questions,
with manual scoring focused on grounding and hallucination avoidance, covering:
- Answerable
- Partially answerable
- Unanswerable
- Edge-case (informal language)

Evaluation was manual using a simple rubric:
- ✅ Good
- ⚠️ Partial
- ❌ Poor

📄 **Full evaluation results:**  
See `evaluation/results.md`

**Key Result:**  
✅ **Zero hallucinations observed**

---

## 🚀 How to Run

### 1️⃣ Setup Environment

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
````

### 2️⃣ Set Environment Variable

Create a `.env` file:

```
GEMINI_API_KEY=your_api_key_here
```

### 3️⃣ Run the Q&A System

```bash
python main.py
```

You can ask questions like:

* *What is the refund policy for damaged items?*
* *Can I cancel my order after it ships?*
* *Do you support cryptocurrency payments?*

---

## 🧪 Run Evaluation

To run the evaluation script:

```bash
python -m evaluation.evaluation
```

This will:

* Ask predefined questions
* Display answers, sources, and retrieval scores
* Allow manual scoring
* Use the same RAG pipeline as the main app

---

## 🔍 Design Trade-offs

* **Safety over completeness:**
  The system prefers declining answers rather than hallucinating.

* **Local embeddings:**
  Chosen to avoid API quota limits and ensure reproducibility.

* **Simple architecture:**
  Focused on clarity and reasoning rather than complex frameworks.

---

## 🔮 Future Improvements

With more time, the following enhancements would be added:

* Intent classification for informal queries
* Retrieval reranking using a cross-encoder
* Metadata-based filtering by policy type
* Retry/fallback logic for LLM failures
* Conversational memory for follow-up questions

---

## 🏁 Conclusion

This project demonstrates a **production-oriented RAG system** with strong
grounding, clear prompt design, and careful evaluation.
Rather than optimizing for flashy UI or large datasets, the focus is on
**correctness, safety, and explainability**—key requirements for real-world
AI systems.

---

## 📌 What I’m Most Proud Of

* Zero hallucinations across all evaluated scenarios
* Clear and defensible evaluation methodology
* Prompt engineering that meaningfully improved output quality

## 📌 What I’d Improve Next

* Better intent handling for informal or emotional queries
* More advanced retrieval ranking
* Automated evaluation metrics

```