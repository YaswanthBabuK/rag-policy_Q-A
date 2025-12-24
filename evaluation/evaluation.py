"""
Evaluation Script for RAG System
"""

from dotenv import load_dotenv
load_dotenv()

import json
from src.rag import PolicyRAG
from src.prompts import prompt_v1, prompt_v2


# ---------------- Test Questions ----------------

EVAL_QUESTIONS = [
    {
        "question": "What is the refund policy for damaged items?",
        "category": "answerable",
        "expected": "Should mention refund or replacement and a contact time window"
    },
    {
        "question": "How long does standard shipping take?",
        "category": "answerable",
        "expected": "Should mention shipping timeframes"
    },
    {
        "question": "Can I cancel my order after it ships?",
        "category": "partially_answerable",
        "expected": "Policy may not clearly define post-shipping cancellation"
    },
    {
        "question": "What are the international shipping rates?",
        "category": "partially_answerable",
        "expected": "May mention availability but not exact rates"
    },
    {
        "question": "Do you offer same-day delivery?",
        "category": "partially_answerable",
        "expected": "Likely not mentioned explicitly"
    },
    {
        "question": "What is your employee vacation policy?",
        "category": "unanswerable",
        "expected": "Outside the scope of customer policy documents"
    },
    {
        "question": "How do I bake a cake?",
        "category": "unanswerable",
        "expected": "Completely unrelated"
    },
    {
        "question": "I need to return something urgently!!!",
        "category": "edge_case",
        "expected": "Should interpret intent as refund/return request"
    }
]


# ---------------- Evaluation Functions ----------------

def evaluate_answer(question_data, result):
    print("\n" + "=" * 80)
    print(f"Question: {question_data['question']}")
    print(f"Category: {question_data['category']}")
    print("-" * 80)

    print(f"Answer: {result['answer']}")
    print(f"Confidence: {result.get('confidence', 'N/A')}")
    print(f"Sources Cited: {result.get('sources_cited', [])}")
    print(f"Retrieval Scores: {[f'{s:.3f}' for s in result.get('retrieval_scores', [])]}")
    print(f"Expected: {question_data['expected']}")

    print("\nEvaluation Criteria:")
    print("✅ Good: Accurate, grounded, appropriate sources")
    print("⚠️  Partial: Somewhat helpful but missing clarity")
    print("❌ Poor: Hallucinated or incorrect")

    score = input("\nYour score (g/p/b): ").strip().lower()
    notes = input("Notes (optional): ").strip()

    score_map = {'g': '✅', 'p': '⚠️', 'b': '❌'}

    return {
        "question": question_data['question'],
        "category": question_data['category'],
        "score": score_map.get(score, '❓'),
        "confidence": result.get('confidence', 'N/A'),
        "sources_cited": result.get('sources_cited', []),
        "retrieval_quality": check_retrieval_quality(result.get('retrieval_scores', [])),
        "notes": notes
    }


def check_retrieval_quality(scores):
    if not scores:
        return "No scores"

    avg = sum(scores) / len(scores)

    if avg < 0.5:
        return "✅ Excellent"
    elif avg < 1.0:
        return "✅ Good"
    elif avg < 1.5:
        return "⚠️ Weak"
    else:
        return "❌ Poor"


# ---------------- Main Evaluation ----------------

def run_evaluation(prompt_version="v2"):
    rag = PolicyRAG()
    docs = rag.load_documents()
    chunks = rag.chunk_documents(docs)
    rag.create_vectorstore(chunks)

    prompt_fn = prompt_v2 if prompt_version == "v2" else prompt_v1

    results = []
    for q in EVAL_QUESTIONS:
        result = rag.answer(q["question"], prompt_fn)
        results.append(evaluate_answer(q, result))

    return results


if __name__ == "__main__":
    print("\nRAG Evaluation")
    print("1. Evaluate V2 (recommended)")
    print("2. Evaluate V1")
    print("3. Compare V1 vs V2")

    choice = input("\nChoice (1/2/3): ").strip()

    if choice == "1":
        run_evaluation("v2")
    elif choice == "2":
        run_evaluation("v1")
    else:
        run_evaluation("v2")
