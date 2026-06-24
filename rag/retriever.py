import os
import re
import shutil
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
 
 
def _parse_groups_block(text: str) -> list[str]:
    chunks = []
    pattern = re.compile(
        r"(GRUPO\s+[A-Z]+)\s*\n((?:[^\n]+\n?){2,6})",
        re.IGNORECASE,
    )
    for match in pattern.finditer(text):
        header = match.group(1).strip()
        body   = match.group(2).strip()
        teams  = [t.strip() for t in body.splitlines() if t.strip()]
 
        if len(teams) < 2:
            continue
 
        letter = header.split()[-1].upper()
        teams_str = ", ".join(teams[:-1]) + " e " + teams[-1]
        main = f"{header} da Copa do Mundo 2026: {teams_str}. "
 
        extras = []
        for team in teams:
            others = [t for t in teams if t != team]
            others_str = ", ".join(others[:-1]) + " e " + others[-1]
            extras.append(
                f"{team} está no Grupo {letter} da Copa 2026 "
                f"ao lado de {others_str}."
            )
 
        chunk = main + " ".join(extras)
        chunks.append(chunk)
 
    return chunks
 
 
def _generic_chunks(text: str) -> list[str]:
    return [
        p.strip()
        for p in text.split("\n\n")
        if len(p.strip()) > 40
    ]
 
 
def _split_document(text: str) -> list[str]:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    group_chunks = _parse_groups_block(text)
 
    cleaned = re.sub(
        r"(GRUPO\s+[A-Z]+\s*\n(?:[^\n]+\n?){2,6})",
        "",
        text,
        flags=re.IGNORECASE,
    )
 
    generic = _generic_chunks(cleaned)
    return group_chunks + generic
 
 
def ingest_documents(force_reindex=False):
    global _collection
 
    if force_reindex and os.path.exists(CHROMA_PATH):
        print(f"{Fore.YELLOW}[RAG] Removendo base vetorial antiga...{Style.RESET_ALL}")
        shutil.rmtree(CHROMA_PATH)
        _collection = None
 
    collection = get_collection()
    model = get_model()
 
    if collection.count() > 0:
        print(
            f"{Fore.GREEN}[RAG] Base vetorial já indexada "
            f"({collection.count()} chunks).{Style.RESET_ALL}"
        )
        return
 
    print(f"{Fore.CYAN}[RAG] Indexando base de conhecimento...{Style.RESET_ALL}")
 
    all_chunks: list[str] = []
    all_ids:    list[str] = []
    chunk_id = 0
 
    for filename in sorted(os.listdir(KNOWLEDGE_PATH)):
        if not filename.endswith(".txt"):
            continue
 
        filepath = os.path.join(KNOWLEDGE_PATH, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
 
        chunks = _split_document(text)
 
        for chunk in chunks:
            all_chunks.append(chunk)
            all_ids.append(f"chunk_{chunk_id}")
            chunk_id += 1
 
    embeddings = model.encode(all_chunks).tolist()
 
    collection.add(
        documents=all_chunks,
        embeddings=embeddings,
        ids=all_ids,
    )
 
    print(
        f"{Fore.GREEN}[RAG] {len(all_chunks)} chunks indexados com sucesso!{Style.RESET_ALL}"
    )
 
 
def retrieve(query: str, n_results: int = 8) -> list[str]:
    collection = get_collection()
    model = get_model()
 
    query_embedding = model.encode([query]).tolist()
 
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results,
    )
 
    return results.get("documents", [[]])[0]