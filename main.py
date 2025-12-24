from dotenv import load_dotenv
load_dotenv()

from src.rag import PolicyRAG
from src.prompts import prompt_v2


def print_result(result):
    """Pretty print the RAG result"""
    print("\n" + "="*80)
    print("ANSWER:")
    print("-"*80)
    print(result.get("answer", ""))
    print("-"*80)
    print(f"Confidence: {result.get('confidence', 'unknown')}")

    # ✅ FIXED: use sources_cited
    sources = result.get("sources_cited", [])
    if sources:
        print(f"Sources Used: {', '.join(sources)}")
    else:
        print("Sources Used: None")

    # Show retrieval quality
    scores = result.get('retrieval_scores', [])
    if scores:
        avg_score = sum(scores) / len(scores)
        quality = (
            "Excellent" if avg_score < 0.5
            else "Good" if avg_score < 1.0
            else "Weak" if avg_score < 1.5
            else "Poor"
        )
        print(f"Retrieval Quality: {quality} (avg score: {avg_score:.3f})")

    print("="*80)


def main():
    print("="*80)
    print("Policy RAG Question-Answering System")
    print("="*80)
    print("\nInitializing...")
    
    rag = PolicyRAG()

    # Load and process documents
    docs = rag.load_documents()
    chunks = rag.chunk_documents(docs)
    rag.create_vectorstore(chunks)

    print("\n✅ System ready! Ask questions about company policies.")
    print("Commands: 'exit' to quit, 'help' for tips\n")

    while True:
        q = input("💬 Your question: ").strip()
        
        if not q:
            continue
            
        if q.lower() == "exit":
            print("\n👋 Goodbye!")
            break
            
        if q.lower() == "help":
            print("\n📚 Tips:")
            print("  - Ask about refund, shipping, or cancellation policies")
            print("  - Be specific: 'What is the refund period?' vs 'Tell me about refunds'")
            print("  - Try edge cases: 'I want my money back!!!'")
            print("  - Test with unrelated questions to see how it handles them")
            continue

        # Get answer
        result = rag.answer(q, prompt_v2)
        print_result(result)


if __name__ == "__main__":
    main()