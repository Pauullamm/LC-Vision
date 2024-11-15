import requests
import fitz  # PyMuPDF
import os

def chunk_pdf_from_url(url, chunk_size=400, overlap=50):
    """
    Download a PDF from the given URL, extract the text, and chunk it into smaller segments.
    
    Parameters:
    - url (str): The URL of the PDF file.
    - chunk_size (int): The target size of each chunk in words (default: 400).
    - overlap (int): The number of overlapping words between chunks (default: 50).
    
    Returns:
    - List of chunks: List of text chunks from the PDF.
    """
    
    # Step 1: Download the PDF from the URL
    r = requests.get(url)
    path = f'{url.replace("https://", "").replace("/", "_")}.pdf'

    with open(path, 'wb') as f:
        f.write(r.content)

    # Step 2: Open the PDF using PyMuPDF (fitz)
    with fitz.open(path) as doc:  # This ensures the file is properly closed
        # Step 3: Extract text from each page
        full_text = ""
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            full_text += page.get_text()

    # Step 4: Tokenize the text into words
    words = full_text.split()

    # Step 5: Chunk the text into smaller pieces
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)
    
    # Step 6: Clean up by removing the downloaded PDF file
    os.remove(path)

    return chunks

# # Example usage:
# url = "your_pdf_url_here"
# chunks = chunk_pdf_from_url(url, chunk_size=400, overlap=50)

# # Print the first 2 chunks to check
# for i, chunk in enumerate(chunks[:2]):
#     print(f"Chunk {i+1}:")
#     print(chunk)
#     print("-" * 80)
