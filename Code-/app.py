import sys
from pathlib import Path
import streamlit as st
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from Code.ingestion import extract_pdf
from Code.utils import chunk_records
from Code.embeddings import Embedder
from Code.vector_store import VectorStore
from Code.rag_pipeline import answer_question
from Code.llm_provider import status
from Code.evaluation import run_evaluation
from Code.config import INPUT_DIR

st.set_page_config(page_title="AUTOSAR HLD Assistant", layout="wide")
st.title("AUTOSAR HLD Document Analysis Assistant")
st.caption("AI-powered document analysis using Retrieval-Augmented Generation")
if "info" not in st.session_state: st.session_state.info = None
if "store" not in st.session_state:
    try: st.session_state.store = VectorStore()
    except Exception as exc: st.error(f"Vector database is unavailable: {exc}")

with st.sidebar:
    uploaded = st.file_uploader("Upload HLD PDF", type="pdf")
    top_k = st.slider("Retrieved chunks", 3, 5, 4)
    st.info(f"Model status: {status()}")
    if st.button("Build / Rebuild Knowledge Base", type="primary"):
        source = uploaded
        if source:
            target = INPUT_DIR / source.name
            target.write_bytes(source.getvalue())
        else:
            target = INPUT_DIR / "sample_hld.pdf"
        try:
            records, meta = extract_pdf(target)
            chunks = chunk_records(records)
            with st.spinner("Creating embeddings and local index..."):
                embedder = Embedder(); st.session_state.store.rebuild(chunks, embedder.encode([c["text"] for c in chunks]))
            st.session_state.info = {"file":target.name,"pages":meta["pages"],"chunks":len(chunks)}
            st.success("Knowledge base built successfully.")
        except Exception as exc: st.error(str(exc))

st.header("Document Information")
info = st.session_state.info
count = st.session_state.store.count() if "store" in st.session_state else 0
if info: st.write(f"**File:** {info['file']}  |  **Pages:** {info['pages']}  |  **Chunks:** {info['chunks']}  |  **Indexed documents:** {count}")
else: st.write(f"No document built in this session. Local vector entries: {count}.")
st.header("Ask a Question")
question = st.text_input("Ask a question about the HLD...", placeholder="What is the purpose of the Communication Manager?")
if st.button("Analyze"):
    try:
        result = answer_question(question, Embedder(), st.session_state.store, top_k)
        st.header("AI Answer"); st.write(result["answer"]); st.caption(f"Response mode: {result['mode']}")
        st.header("Evidence / Citations")
        for i,e in enumerate(result["evidence"],1):
            with st.expander(f"{i}. {e['source']} — Page {e['page']} — {e['section']}"): st.write(e["text"])
    except Exception as exc: st.error(str(exc))
st.header("Evaluation")
if st.button("Run Evaluation"):
    try:
        metrics = run_evaluation(Embedder(), st.session_state.store)
        st.json(metrics)
        st.caption("Prototype metrics: retrieval/page matching, citation presence, and keyword coverage. They are not a substitute for human evaluation.")
    except Exception as exc: st.error(f"Evaluation could not run: {exc}")
