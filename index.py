import os
import json
import subprocess
from pypdf import PdfReader
from pyserini.search.lucene import LuceneSearcher
from tqdm import tqdm  # This creates the progress bar

# --- CONFIGURATION ---
PDF_FOLDER = "pdf_corpus"
INDEX_DIR = "indexes/my_lucene_index"
TEMP_JSON_FILE = "corpus.jsonl"

def get_pdf_text_with_progress(folder):
    """Reads PDFs and updates a progress bar."""
    if not os.path.exists(folder):
        print(f"Error: Folder '{folder}' does not exist.")
        return

    files = [f for f in os.listdir(folder) if f.endswith(".pdf")]
    total_files = len(files)
    
    if total_files == 0:
        print("No PDFs found!")
        return

    print(f"\n[1/3] Reading {total_files} PDFs...")

    # tqdm creates the visual progress bar
    for filename in tqdm(files, unit="pdf"):
        path = os.path.join(folder, filename)
        try:
            reader = PdfReader(path)
            text = ""
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + " "
            
            yield {
                "id": filename,
                "contents": text
            }
        except Exception as e:
            # We print error to stderr so it doesn't break the progress bar layout
            tqdm.write(f"  Warning: Could not read {filename} ({e})")

if __name__ == "__main__":
    
    # --- Step 1: Convert PDFs to JSONL ---
    # We clear the temp file first
    if os.path.exists(TEMP_JSON_FILE):
        os.remove(TEMP_JSON_FILE)

    count = 0
    with open(TEMP_JSON_FILE, "w") as f:
        # Loop through PDFs with the progress bar
        for doc in get_pdf_text_with_progress(PDF_FOLDER):
            f.write(json.dumps(doc) + "\n")
            count += 1
    
    print(f"✓ Saved {count} documents to temporary file.")

    # --- Step 2: Build Lucene Index ---
    print("\n[2/3] Launching Java Indexer (this takes 10-20 seconds)...")
    print("      (You will see a lot of scrolling text now - this is good!)")
    
    cmd = [
        "python", "-m", "pyserini.index.lucene",
        "--collection", "JsonCollection",
        "--input", ".",
        "--index", INDEX_DIR,
        "--generator", "DefaultLuceneDocumentGenerator",
        "--threads", "1",
        "--storePositions", "--storeDocvectors", "--storeRaw"
    ]
    
    # Run and allow output to stream to console so you see it working
    process = subprocess.run(cmd)
    
    if process.returncode != 0:
        print("\n❌ Indexing Failed! (Did you set the JAVA_HOME path?)")
        exit(1)
    
    print("\n✓ Indexing Complete!")

    # --- Step 3: Search ---
    print("\n[3/3] Verifying Index with a Search...")
    try:
        searcher = LuceneSearcher(INDEX_DIR)
        query = "machine learning"
        hits = searcher.search(query)

        print(f"\n--- Results for '{query}' ---")
        if len(hits) == 0:
            print("No results found.")
        
        for i in range(len(hits)):
            print(f"{i+1}. {hits[i].docid} (Score: {hits[i].score:.4f})")
            
    except Exception as e:
        print(f"Search failed: {e}")