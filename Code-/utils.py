from .config import CHUNK_SIZE, CHUNK_OVERLAP

def chunk_records(records, size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    chunks = []
    for record in records:
        text, start, index = record["text"], 0, 0
        while start < len(text):
            end = min(len(text), start + size)
            if end < len(text):
                boundary = text.rfind(". ", start, end)
                if boundary > start + size // 2: end = boundary + 1
            chunk = text[start:end].strip()
            if chunk:
                chunks.append({**record, "chunk_id": f"{record['source']}_p{record['page']}_{index}", "text": chunk})
                index += 1
            if end >= len(text): break
            start = max(end - overlap, start + 1)
    return chunks
