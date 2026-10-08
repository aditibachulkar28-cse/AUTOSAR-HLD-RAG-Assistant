"""PDF extraction with page and likely section metadata."""
from pathlib import Path
import fitz

def _section(text: str) -> str:
    for line in text.splitlines()[:12]:
        line = line.strip()
        if line and (line[:1].isdigit() or line.isupper() or line.startswith("#")):
            return line.lstrip("# ")[:100]
    return "General"

def extract_pdf(pdf_path):
    path = Path(pdf_path)
    if not path.exists() or path.suffix.lower() != ".pdf":
        raise ValueError("Please provide a valid PDF file.")
    try:
        document = fitz.open(path)
    except Exception as exc:
        raise ValueError(f"Could not open PDF: {exc}") from exc
    records = []
    for number, page in enumerate(document, start=1):
        text = page.get_text("text").strip()
        if text:
            records.append({"source": path.name, "page": number, "section": _section(text), "text": text})
    metadata = document.metadata or {}
    page_count = len(document)
    document.close()
    if not records:
        raise ValueError("The PDF has no extractable text.")
    return records, {"pages": page_count, "metadata": metadata}
