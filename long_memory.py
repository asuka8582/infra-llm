import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class LongTermMemory:
    """
    Manages long-term memory using vector embeddings and FAISS.
    """
    def __init__(self, storage_dir="ltm_data", model_name="paraphrase-multilingual-MiniLM-L12-v2"):
        self.storage_dir = storage_dir
        self.index_path = os.path.join(storage_dir, "faiss_index.bin")
        self.docs_path = os.path.join(storage_dir, "documents.json")

        # Initialize embedding model
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()

        # Initialize or load index and documents
        if not os.path.exists(storage_dir):
            os.makedirs(storage_dir)

        if os.path.exists(self.index_path) and os.path.exists(self.docs_path):
            self.index = faiss.read_index(self.index_path)
            with open(self.docs_path, "r", encoding="utf-8") as f:
                self.documents = json.load(f)
        else:
            self.index = faiss.IndexFlatL2(self.dimension)
            self.documents = []

    def add_memory(self, text):
        """
        Adds a new piece of information to the long-term memory.
        """
        if not text.strip():
            return

        embedding = self.model.encode([text])
        self.index.add(np.array(embedding).astype("float32"))
        self.documents.append(text)
        self.save()

    def query_memory(self, query, top_k=3):
        """
        Retrieves the most relevant memories for a given query.
        """
        if not self.documents:
            return ""

        embedding = self.model.encode([query])
        distances, indices = self.index.search(np.array(embedding).astype("float32"), top_k)

        results = []
        for idx in indices[0]:
            if idx != -1 and idx < len(self.documents):
                results.append(self.documents[idx])

        return "\n---\n".join(results)

    def save(self):
        """
        Persists the index and documents to disk.
        """
        faiss.write_index(self.index, self.index_path)
        with open(self.docs_path, "w", encoding="utf-8") as f:
            json.dump(self.documents, f, ensure_ascii=False, indent=2)
