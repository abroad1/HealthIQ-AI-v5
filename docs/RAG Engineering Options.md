# 🧩 RAG Engineering Options — Brainstorming Note

> **Purpose**: Capture current thinking on Retrieval-Augmented Generation (RAG) for HealthIQ AI.  
> This is not a final design — it’s a placeholder to guide future iteration.

---

## 📌 Options for Implementing RAG

### Option A — RAG-lite (Prompt Stuffing)
- **Description**: Pass curated text blocks (biomarker explainers, cluster rules) directly into Gemini prompts.
- ✅ **Pros**: Simple, no infra, fast to ship.  
- ❌ **Cons**: Doesn’t scale, risks token bloat, limited retrieval quality.

### Option B — Local Vector Store (FAISS/Chroma)
- **Description**: Embed chunks locally; retrieve top-k inside FastAPI.
- ✅ **Pros**: Cheap, low latency, fully under control.  
- ❌ **Cons**: Harder to scale, limited metadata filters, more ops overhead later.

### Option C — Postgres + pgvector (Supabase)
- **Description**: Store embeddings + metadata in Supabase Postgres with pgvector.
- ✅ **Pros**: Fits our stack, strong SQL filtering (biomarker_id, persona, source), reliable ops.  
- ❌ **Cons**: Slightly more complex queries; may need reranking at scale.

### Option D — Managed Vector DB (Pinecone/Weaviate/Qdrant)
- **Description**: External vector database with advanced retrieval features.
- ✅ **Pros**: Scales easily, richer retrieval features, strong observability.  
- ❌ **Cons**: Cost, vendor lock-in, PHI/data governance review required.

### Option E — Hybrid Retrieval (BM25 + Embeddings + Reranker)
- **Description**: Combine text search + vector retrieval, rerank with a cross-encoder or LLM.
- ✅ **Pros**: Best factual precision; covers both semantic and lexical matches.  
- ❌ **Cons**: More plumbing, slightly higher latency.

---

## 🔍 Quality Gate & Iteration

- **Rule-based checks**: All driver biomarkers covered, no contradictions, citations included.  
- **Optional LLM-as-judge**: Secondary validation for coherence/completeness.  
- **Iteration policy**:  
  - Pass → accept first draft.  
  - Fail → run one refinement pass with missing context injected.  
  - Cap iterations at 2 total.

---

## ⚖️ Data Governance

- ✅ Store only curated knowledge (no PHI) in RAG index.  
- ✅ Each chunk tagged with biomarker_id, cluster, persona, citation_id.  
- ✅ Versioning: valid_from / valid_to for sources.  
- ✅ Ensure outputs cite retrieved chunks (traceability).

---

## 🚀 Current Recommendation

- **Baseline**: Option C (Supabase + pgvector)  
- **Enhancement**: Add hybrid retrieval (Option E) for higher precision.  
- **Scope**: Limit initial corpus to biomarker explainers, cluster rules, lifestyle libraries, and guideline excerpts.  
- **Future**: Evaluate managed DBs (Option D) only if scale/latency require it.

---

**Status**: Draft v0.1 (brainstorming only)  
**Next Review**: When Gemini refinement/RAG integration is scoped (post-MVP)  
