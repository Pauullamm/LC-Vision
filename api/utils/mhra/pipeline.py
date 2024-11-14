import pandas as pd
from upsert import upsert_to_pinecone
import concurrent.futures
import time

# Assuming chunk_pdf_from_url and upsert_to_pinecone are defined elsewhere
from chunking import chunk_pdf_from_url


# Function to process one document: chunk, embed, and upsert
def process_document(test_url, test_drug_name, test_doc_type):
    # Get pdf text from URL and chunk it into around 400 words each
    chunks = chunk_pdf_from_url(test_url)

    # Upsert the data to Pinecone (pass chunks with metadata)
    upsert_to_pinecone(chunks, test_url, test_drug_name, test_doc_type)
    print(f"Document from {test_url} has been processed and upserted.")


def parallel_upload(df, max_workers=10):
    # Initialize ThreadPoolExecutor with max_workers
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # List to hold all futures
        futures = []

        # Iterate through the rows in the dataframe (document metadata)
        for _, row in df.iterrows():
            # Extract necessary metadata for each document
            url = row['metadata_storage_path']
            product_name = row['product_name']
            doc_type = row['doc_type']

            # Submit the processing task for each document to the executor
            futures.append(executor.submit(process_document, url, product_name, doc_type))

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
