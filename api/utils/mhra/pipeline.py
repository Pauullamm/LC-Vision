import pandas as pd
from upsert import upsert_to_pinecone
import concurrent.futures
import time
from chunking import chunk_pdf_from_url
import numpy as np

# Function to retrieve one document, generate chunks, embed, and upsert
def process_document(url, drug_name, doc_type):
    # Get pdf text from URL and chunk it into around 400 words each
    try:
        print(f'processing document {drug_name} at {url}')
        chunks = chunk_pdf_from_url(url)


        for chunk in chunks:
            # Upsert the data to Pinecone (pass chunks with metadata)
            upsert_to_pinecone(chunk, url, drug_name, doc_type)
            print(f"Document of doc_type {doc_type} and product name {drug_name} has been processed and upserted.")
    except Exception as e:
        print(f'Error processing document {drug_name} at {url}: {e}')


def process_chunk(df_chunk):
    for _, row in df_chunk.iterrows():
        url = row['metadata_storage_path']
        product_name = row['product_name']
        doc_type = row['doc_type']
        process_document(url, product_name, doc_type)


def parallel_upload(df, max_workers=10):
    # Divide dataframe into chunks for workers to work on in parallel
    df_splits = np.array_split(df, max_workers)
    # Initialize ThreadPoolExecutor with max_workers
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # List to hold all futures
        futures = []
        # Iterate through the rows in the dataframe (document metadata)
        for split in df_splits:
            # Submit the processing task for each chunk to the executor
            futures.append(executor.submit(process_chunk, split))

        # Wait for all futures to complete
        for future in concurrent.futures.as_completed(futures):
            try:
                # Wait for the thread to complete and get the result
                future.result()
            except Exception as e:
                print(f"Error processing document: {e}")

    print("All documents have been processed and upserted to Pinecone.")


# Main code to run the parallel upload
if __name__ == "__main__":
    file_path = ''
    df = pd.read_csv(file_path)

    # Start the parallel upload process
    start_time = time.time()
    parallel_upload(df, max_workers=10)
    end_time = time.time()

    execution_time = end_time - start_time
    print(f"Total time taken: {execution_time / 3600:.2f} hours")
