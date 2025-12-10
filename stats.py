from pyserini.index.lucene import IndexReader

# Point to your index folder
INDEX_DIR = "indexes/my_lucene_index"

try:
    # Load the index reader (allows direct access to the database)
    reader = IndexReader(INDEX_DIR)
    print(f"Index loaded from: {INDEX_DIR}")
    
    while True:
        query = input("\nEnter a word to analyze (or 'exit'): ").strip().lower()
        if query == 'exit': 
            break
        if not query: 
            continue

        # 1. Analyze the word (Transform "Learning" -> "learn" to match index)
        # The index stores stemmed words, so we must stem the input first.
        analyzed_tokens = reader.analyze(query)
        
        if not analyzed_tokens:
            print("  This word was removed during preprocessing (e.g., it's a stop word).")
            continue
            
        term = analyzed_tokens[0] # Take the first token
        print(f"  (Searching for index term: '{term}')")

        # 2. Get the Postings List (The raw list of docs containing the term)
        # This returns a list of objects containing {docid, tf, positions}
        postings = reader.get_postings_list(term)

        if postings is None:
            print(f"  Term '{term}' not found in any document.")
        else:
            # 3. Print Document Frequency (DF)
            df = len(postings)
            print(f"  -> Found in {df} documents total.")
            
            print(f"  -> Breakdown:")
            print(f"     {'FILENAME':<30} | {'COUNT (TF)':<10}")
            print(f"     {'-'*30} | {'-'*10}")
            
            # 4. Loop through each document and print Term Frequency (TF)
            for posting in postings:
                # Convert internal ID (integer) back to filename (string)
                filename = reader.convert_internal_docid_to_collection_docid(posting.docid)
                tf = posting.tf  # Term Frequency
                
                print(f"     {filename:<30} | {tf:<10}")

except Exception as e:
    print(f"Error: {e}")