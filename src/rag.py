import os
import json
from pathlib import Path
from google import genai

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings


# ---------------- Local Embeddings (Quota-safe) ----------------

def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


# ---------------- RAG System ----------------

class PolicyRAG:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not set")

        self.client = genai.Client(api_key=api_key)

        # Stable, tested free-tier model
        self.model_name = "gemini-2.5-flash"

        self.vectorstore = None

    def load_documents(self, path="data"):
        docs = []
        for file in Path(path).glob("*.txt"):
            with open(file, "r", encoding="utf-8") as f:
                docs.append(
                    Document(
                        page_content=f.read(),
                        metadata={"source": file.name}
                    )
                )
        print(f"✅ Loaded {len(docs)} documents")
        return docs

    def chunk_documents(self, documents):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        chunks = splitter.split_documents(documents)
        print(f"✅ Created {len(chunks)} chunks")
        return chunks

    def create_vectorstore(self, chunks):
        print("Creating vector store...")
        self.vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=get_embeddings(),
            collection_name="policy_docs"
        )
        print("✅ Vector store created")

def answer(self, question, prompt_fn, k=3):
    if not self.vectorstore:
        return {
            "answer": "Vector store not initialized.",
            "confidence": "low",
            "sources_cited": [],
            "retrieval_scores": []
        }

    results = self.vectorstore.similarity_search_with_score(question, k=k)

    if not results:
        return {
            "answer": "I could not find relevant information in the policy documents to answer this question.",
            "confidence": "low",
            "sources_cited": [],
            "retrieval_scores": []
        }

    docs = [doc for doc, score in results]
    scores = [score for doc, score in results]

    min_score = min(scores)

    # Case 1: Completely out of scope
    if min_score > 1.7:
        return {
            "answer": "This question is outside the scope of the policy documents.",
            "confidence": "low",
            "sources_cited": [],
            "retrieval_scores": scores
        }

    # Case 2: Policy-related but info not available
    if min_score > 1.2:
        return {
            "answer": "I could not find relevant information in the policy documents to answer this question.",
            "confidence": "low",
            "sources_cited": [],
            "retrieval_scores": scores
        }

    # Valid policy question → use LLM
    context_parts = []
    for i, doc in enumerate(docs, 1):
        source = doc.metadata.get("source", "Unknown")
        context_parts.append(f"[Source {i}: {source}]\n{doc.page_content}")

    context = "\n\n---\n\n".join(context_parts)
    prompt = prompt_fn(context, question)

    try:
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt
        )
    except Exception as e:
        return {
            "answer": f"LLM error: {str(e)}",
            "confidence": "low",
            "sources_cited": [],
            "retrieval_scores": scores
        }

    result = self._parse_response(response.text)

    # Ensure sources exist ONLY for valid answers
    if not result["sources_cited"]:
        result["sources_cited"] = [doc.metadata.get("source") for doc in docs]

    result["retrieval_scores"] = scores
    return result


    def _parse_response(self, text: str):
        try:
            cleaned = text.strip()
            if cleaned.startswith("```"):
                cleaned = cleaned.replace("```json", "").replace("```", "").strip()

            parsed = json.loads(cleaned)
            return {
                "answer": parsed.get("answer", ""),
                "confidence": parsed.get("confidence", "unknown"),
                "sources_cited": parsed.get("sources_cited", [])
            }
        except Exception:
            return {
                "answer": text,
                "confidence": "unknown",
                "sources_cited": []
            }
