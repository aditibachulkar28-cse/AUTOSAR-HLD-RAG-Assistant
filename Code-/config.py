from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[1]
INPUT_DIR = ROOT / "Input_Data"
VECTOR_DB_DIR = ROOT / "vector_db"
EVALUATION_DIR = ROOT / "Evaluation_Results"
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
CHUNK_SIZE = 850
CHUNK_OVERLAP = 150
DEFAULT_TOP_K = 4
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "demo").lower()
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "")
