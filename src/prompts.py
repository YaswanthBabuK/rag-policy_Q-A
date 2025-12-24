"""
Prompt templates for the RAG Policy Assistant.

This file demonstrates prompt iteration:
- v1: Naive baseline
- v2: Improved, production-ready prompt (USED)
- v3: Experimental prompt for future improvements
"""


def prompt_v1(context: str, question: str) -> str:
    """
    Version 1: Basic prompt (baseline)

    Limitations:
    - No hallucination prevention
    - No handling of missing or out-of-scope questions
    - No structured output
    """
    return f"""
Answer the question using the context below.

Context:
{context}

Question:
{question}
"""


def prompt_v2(context: str, question: str) -> str:
    """
    Version 2: Improved prompt with strict grounding and structure

    Key Improvements:
    - Explicit instruction to use ONLY retrieved context
    - Graceful handling of missing or unrelated questions
    - Structured JSON output for reliability
    - Confidence indicator
    - Source citations
    """

    return f"""
You are a policy assistant that answers questions about company policies.

IMPORTANT RULES:
1. Answer ONLY using information from the context provided below.
2. If the context does not contain enough information, say:
   "I could not find this information in the provided policy documents."
3. If the question is completely unrelated to the policies, say:
   "This question is outside the scope of the available policy documents."
4. Do NOT use external knowledge or assumptions.
5. Be clear, factual, and concise.
6. Do NOT wrap the response in markdown or code fences.

CONTEXT:
{context}

QUESTION:
{question}

Respond strictly in the following JSON format:
{{
  "answer": "Your answer here, grounded in the context",
  "confidence": "high | medium | low"
  "sources_cited": []
}}
"""


def prompt_v3_experimental(context: str, question: str) -> str:
    """
    Version 3: Experimental prompt (not used by default)

    Additional features:
    - Explicit reasoning
    - Stronger edge-case handling
    - More verbose output

    Trade-off:
    - Higher token usage
    - Increased parsing complexity
    """

    return f"""
You are a careful and accurate policy assistant.

TASK:
Answer the user's question using ONLY the policy excerpts provided.

STRICT RULES:
1. Do not use any knowledge outside the context.
2. If the answer is missing or unclear, explicitly state that.
3. If the question is unrelated to policy documents, politely decline.
4. Cite the relevant sources by filename.
5. Explain briefly why you chose your confidence level.
6. Do NOT format the response as markdown.

CONTEXT:
{context}

QUESTION:
{question}

Provide your response in JSON:
{{
  "answer": "Grounded answer with source references",
  "confidence": "high | medium | low",
  "reasoning": "Short explanation for confidence level"
}}
"""
