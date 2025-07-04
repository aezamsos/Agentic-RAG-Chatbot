from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import uuid
from utils.mcp import MCPMessage


class RetrievalAgent:
    def __init__(self):
        # Load the sentence embedding model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = None
        self.chunk_map = {}

    def chunk_text(self, text, chunk_size=500):
        """Split large text into smaller chunks for embedding and retrieval."""
        chunks, current = [], ""
        for line in text.split("\n"):
            if len(current) + len(line) < chunk_size:
                current += line + " "
            else:
                chunks.append(current.strip())
                current = line + " "
        if current:
            chunks.append(current.strip())
        return chunks

    def build_index(self, full_text):
        """Build the FAISS index from the provided text."""
        chunks = self.chunk_text(full_text)
        embeddings = self.model.encode(chunks, convert_to_numpy=True)

        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(embeddings)

        # Map index positions to chunks for later retrieval
        for i, chunk in enumerate(chunks):
            self.chunk_map[i] = chunk

    def retrieve(self, query, top_k=3):
        """Retrieve the top K most relevant chunks from the index based on the query."""
        if self.index is None or len(self.chunk_map) == 0:
            raise ValueError("Index is not built or chunk_map is empty. Please run build_index() first.")

        query_vec = self.model.encode([query], convert_to_numpy=True)
        distances, indices = self.index.search(query_vec, top_k)

        # Safely retrieve only valid indices
        top_chunks = [self.chunk_map[i] for i in indices[0] if i in self.chunk_map]

        return MCPMessage(
            sender="RetrievalAgent",
            receiver="LLMResponseAgent",
            type="CONTEXT_RESPONSE",
            trace_id=str(uuid.uuid4()),
            payload={
                "top_chunks": top_chunks,
                "query": query
            }
        ).to_dict()
