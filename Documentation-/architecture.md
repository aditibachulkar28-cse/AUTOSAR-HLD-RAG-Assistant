# System Architecture

```mermaid
flowchart TD
U[User] --> UI[Streamlit UI]
UI --> P[PDF Upload]
P --> X[PDF Text Extraction]
X --> C[Chunking]
C --> E[Sentence Transformer Embeddings]
E --> D[(ChromaDB)]
U --> Q[User Question]
Q --> R[Similarity Retrieval]
D --> R
R --> CT[Relevant Context]
CT --> PR[Strict Prompt]
PR --> L[LLM or Demo Fallback]
L --> A[Grounded Answer with Page/Section Citations]
```

The UI accepts a PDF and questions. Extraction preserves pages; chunking keeps manageable passages; embeddings enable meaning-based matching; ChromaDB retains them locally. Retrieval supplies evidence to a strict prompt. The final response displays only retrieved evidence plus its actual metadata.
