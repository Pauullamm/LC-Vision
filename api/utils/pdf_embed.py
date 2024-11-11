import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer
import numpy as np

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text("text")  # Extract text from each page
    return text

# Function to chunk the text into smaller pieces (e.g., paragraphs or fixed-size chunks)
def chunk_text(text, chunk_size=500):
    """
    Splits the text into smaller chunks. If a chunk is too large, it splits by a sentence or paragraph.
    :param text: The full document text.
    :param chunk_size: The maximum number of characters per chunk.
    :return: A list of text chunks.
    """
    # Split by paragraphs first
    paragraphs = text.split("\n")
    chunks = []
    current_chunk = ""
    
    for paragraph in paragraphs:
        if len(current_chunk) + len(paragraph) <= chunk_size:
            # Add to the current chunk if it's not too long
            current_chunk += paragraph + "\n"
        else:
            # If adding this paragraph exceeds chunk_size, save the current chunk and start a new one
            chunks.append(current_chunk.strip())
            current_chunk = paragraph + "\n"

    # Add any remaining text as the last chunk
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

# Function to embed text chunks using Sentence-BERT
def embed_chunks(chunks, model_name='all-MiniLM-L6-v2'):
    model = SentenceTransformer(model_name)
    embeddings = model.encode(chunks, convert_to_tensor=True)  # Embed the chunks
    return embeddings

# Example usage
if __name__ == "__main__":
    # Path to the PDF document
    pdf_path = 'your_document.pdf'

    # Step 1: Extract text from the PDF
    full_text = extract_text_from_pdf(pdf_path)
    print(f"Extracted text: {full_text[:500]}...")  # Print first 500 characters of extracted text

    # Step 2: Chunk the text into manageable pieces
    chunks = chunk_text(full_text, chunk_size=500)  # 500 characters per chunk
    print(f"Number of chunks: {len(chunks)}")

    # Step 3: Embed the chunks
    embeddings = embed_chunks(chunks)

    # Optional: Convert embeddings to numpy arrays for easier handling
    embeddings_np = embeddings.cpu().detach().numpy()

    print(f"Embedding shape: {embeddings_np.shape}")  # Should be (num_chunks, embedding_dim)

    # For demonstration, print the first chunk and its embedding
    print(f"First chunk: {chunks[0]}")
    print(f"Embedding for the first chunk: {embeddings_np[0]}")
