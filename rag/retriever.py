import os
import chromadb
from sentence_transformers import SentenceTransformer
from colorama import Fore, Style

CHROMA_PATH = "./data/chroma_db"
KNOWLEDGE_PATH = "./data/knowledge_base"
COLLECTION_NAME = "copa2026"

_model = None
_collection = None


def get_model():
    global _model
    if _model is None:
        print(f"{Fore.CYAN}[RAG] Carregando modelo de embeddings...{Style.RESET_ALL}")
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def get_collection():
    global _collection
    if _collection is None:
        client = chromadb.PersistentClient(path=CHROMA_PATH)
        _collection = client.get_or_create_collection(COLLECTION_NAME)
    return _collection


def ingest_documents():
    collection = get_collection()
    model = get_model()

    if collection.count() > 0:
        print(f"{Fore.GREEN}[RAG] Base vetorial já indexada ({collection.count()} chunks).{Style.RESET_ALL}")
        return

    print(f"{Fore.CYAN}[RAG] Indexando base de conhecimento...{Style.RESET_ALL}")

    all_chunks = []
    all_ids = []
    chunk_id = 0

    for filename in os.listdir(KNOWLEDGE_PATH):
        if not filename.endswith(".txt"):
            continue
        filepath = os.path.join(KNOWLEDGE_PATH, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()

        paragraphs = [p.strip() for p in text.split("\n\n") if len(p.strip()) > 30]
        for para in paragraphs:
            all_chunks.append(para)
            all_ids.append(f"chunk_{chunk_id}")
            chunk_id += 1

    embeddings = model.encode(all_chunks).tolist()

    collection.add(
        documents=all_chunks,
        embeddings=embeddings,
        ids=all_ids,
    )

    print(f"{Fore.GREEN}[RAG] {len(all_chunks)} chunks indexados com sucesso!{Style.RESET_ALL}")


def retrieve(query: str, n_results: int = 3) -> list[str]:
    collection = get_collection()
    model = get_model()

    query_embedding = model.encode([query]).tolist()
    results = collection.query(query_embeddings=query_embedding, n_results=n_results)

    documents = results.get("documents", [[]])[0]
    return documents
