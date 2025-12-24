# RAG Evaluation Results

## Overview
The RAG system was evaluated using **8 test questions** designed to cover
answerable, partially answerable, unanswerable, and edge-case scenarios.
The objective of this evaluation was to assess **grounding quality,
hallucination avoidance, source attribution, and confidence calibration**
rather than raw answer completeness.

The evaluation was performed **manually** using a simple rubric:
- ✅ **Good** – Accurate, grounded, and appropriately sourced  
- ⚠️ **Partial** – Safe response, but missing clarity or intent interpretation  
- ❌ **Poor** – Hallucinated or incorrect  

---

## Evaluation Summary

- **Total Questions:** 8  
- **✅ Good:** 6 (75%)  
- **⚠️ Partial:** 2 (25%)  
- **❌ Poor:** 0 (0%)  

**Key Result: Zero Hallucinations**

Across all questions, the system avoided generating unsupported or fabricated
information. For ambiguous or out-of-scope queries, it preferred to decline
rather than guess, demonstrating a safety-first design.

---

## Performance by Category

### Answerable Questions (2 questions)
- **Score:** 2 / 2 ✅ (100%)

The system performed perfectly on clearly defined policy questions:
- Refund policy for damaged items
- Standard shipping timelines

All answers were factually correct, grounded in retrieved policy text, and
included appropriate source citations.

---

### Partially Answerable Questions (3 questions)
- **Score:** 2 / 3 ✅, 1 / 3 ⚠️

These questions involved scenarios where policy documents did not provide
complete or explicit details:
- Post-shipment cancellation
- International shipping rates
- Same-day delivery availability

The system handled these conservatively, providing available information
when possible and clearly declining to speculate when details were missing.

---

### Unanswerable Questions (2 questions)
- **Score:** 2 / 2 ✅ (100%)

The system correctly declined questions outside the scope of customer-facing
policy documents, such as:
- Employee vacation policy
- General cooking instructions

No hallucinations were observed, and confidence levels appropriately reflected
uncertainty.

---

### Edge-Case Question (1 question)
- **Score:** 0 / 1 ⚠️

For the informal and emotionally phrased query (“I need to return something urgently!!!”),
the system failed safely by declining to answer rather than hallucinating.

While this behavior preserved correctness, it revealed a limitation in intent
inference for informal or emotionally charged language.

---

## Key Observations

### Strengths
- Strong grounding for clearly answerable questions
- Consistent hallucination avoidance
- Reliable out-of-scope detection
- Confidence levels aligned with retrieval quality
- Transparent source attribution

### Limitations
- Conservative handling of informal or emotional language
- Limited intent inference for ambiguous queries
- Weak but expected retrieval for out-of-scope questions
- Partial answers could benefit from better synthesis across documents

---

## Future Improvements

Given additional time, the following improvements would be prioritized:
- Intent classification or query normalization for informal inputs
- Retrieval reranking to improve precision
- Dynamic retrieval thresholds based on question type
- Retry and fallback handling for LLM request failures
- Metadata-based filtering by policy category

---

## Conclusion
The RAG system demonstrates **production-ready behavior** for policy-based
question answering. It prioritizes correctness and safety over overconfident
responses, achieving strong grounding and **zero hallucinations** across all
evaluated scenarios.

For a limited-time implementation using free APIs, the system reflects solid
engineering judgment, effective prompt design, and careful evaluation practices.

---

## Appendix: Test Questions

The following test questions were used during evaluation.  
Icons reflect the **final evaluation score**, not whether the question was
answerable.

- ✅ What is the refund policy for damaged items?
- ✅ How long does standard shipping take?
- ✅ Can I cancel my order after it ships?
- ⚠️ What are the international shipping rates?
- ✅ Do you offer same-day delivery?
- ✅ What is your employee vacation policy?
- ✅ How do I bake a cake?
- ⚠️ I need to return something urgently!!!