# AUTOSAR HLD Document Analysis Assistant

## Problem, Aim, and Case Study
Architecture documents can be hard to search during design review. This student prototype uses Retrieval-Augmented Generation (RAG) to answer questions about a fictional AUTOSAR-style High-Level Design (HLD), with evidence and page/section citations. Its aim is quick evidence-based document analysis, not automotive engineering automation.

## Objectives
Extract PDF text, preserve page metadata, chunk and embed it, search a local vector database, present grounded cited answers, and evaluate predefined questions.

## Why RAG?
RAG retrieves relevant document passages before an answer is created. This makes the response traceable to uploaded evidence and reduces unsupported answers. Embeddings are numeric semantic representations of text. `all-MiniLM-L6-v2` is a compact, widely used sentence embedding model suitable for local prototype search.

## Technology Stack
Python, Streamlit, PyMuPDF, sentence-transformers, ChromaDB, pandas, and optional matplotlib. The local demo fallback works without a paid API.

## Folder Structure
`Code/` contains the app and pipeline; `Input_Data/` contains fictional input; `Model_Prompts_Config/` contains configuration; `Evaluation_Results/` holds questions/results; `Documentation/` holds submission material.

## Installation and Run (Windows)
```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python Code\create_sample_pdf.py
streamlit run Code\app.py
```
If `python` points to the Windows Store placeholder, install Python 3.10–3.13 from python.org and reopen the terminal.

## How to Demonstrate
1. Start the app and select **Build / Rebuild Knowledge Base** (the provided synthetic PDF is used if no upload is selected).
2. Ask a question such as “What is the purpose of the Communication Manager?”
3. Read the answer and expand **Evidence / Citations** to show page/section proof.
4. Run Evaluation to create actual results files.

## Citations and Evaluation
Citations are constructed from retrieved chunk metadata; page numbers are never invented. Evaluation checks expected-page retrieval, citation presence, and simple keyword coverage. These are prototype metrics and not equivalent to human evaluation.

## Limitations and Future Scope
The sample is fictional, text-only PDFs work best, and the demo fallback is extractive rather than a full LLM. Retrieval quality depends on document quality. Future work could add human-reviewed answer scoring and secure, approved model hosting.

## External API Declaration and Responsible AI
No API key is required for demo mode. To use the optional API, set variables from `Model_Prompts_Config/.env.example`; the submitter must declare that dependency. Outputs require human review and must not be used to approve real automotive designs.
