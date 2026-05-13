import PyPDF2

def extract_text(uploaded_file) -> str:
    reader = PyPDF2.PdfReader(uploaded_file)
    return "\n".join(page.extract_text() for page in reader.pages)

def chunk_text(text: str, chunk_size: int = 3000) -> list[str]:
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i:i + chunk_size]))
    return chunks