import arxiv
import os
import time
import sys

# Create a directory for the corpus
output_dir = "pdf_corpus"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Construct the search query
client = arxiv.Client()
search = arxiv.Search(
    query = "machine learning",
    max_results = 100,
    sort_by = arxiv.SortCriterion.SubmittedDate
)

print(f"Downloading 100 PDFs to '{output_dir}'...")
print("Step 1: Fetching metadata from ArXiv... (This may take a few seconds)")

# 1. VISIBLE FETCHING
try:
    results = list(client.results(search))
    print(f"Metadata fetched successfully! Found {len(results)} papers.")
except Exception as e:
    print(f"Error fetching metadata: {e}")
    sys.exit(1)

count = 0

for i, result in enumerate(results):
    try:
        # Create a valid filename
        filename = f"{result.entry_id.split('/')[-1]}.pdf"
        file_path = os.path.join(output_dir, filename)
        
        # 1. SKIP IF EXISTS
        if os.path.exists(file_path):
            count += 1
            print(f"[{count}/100] [Skipping] Already exists: {result.title[:50]}...")
            continue

        # 2. RETRY LOGIC
        retries = 3
        while retries > 0:
            try:
                print(f"[{count + 1}/100] Downloading: {result.title[:50]}...")
                result.download_pdf(dirpath=output_dir, filename=filename)
                count += 1
                
                # 3. VISIBLE SLEEP
                print("   -> Success. Cooling down for 3 seconds...", end=" ", flush=True)
                time.sleep(3) 
                print("Done.")
                break 
            
            except Exception as e:
                retries -= 1
                print(f"\n   -> Error: {e}")
                if retries > 0:
                    print(f"   -> Retrying in 10s... ({retries} attempts left)", flush=True)
                    time.sleep(10)
        
        if retries == 0:
            print(f"   -> FAILED to download: {result.title}")

    except Exception as main_e:
        print(f"Critical error processing result: {main_e}")

print("\nAll Done!")