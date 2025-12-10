import streamlit as st
import os
from pyserini.search.lucene import LuceneSearcher

# --- CONFIGURATION ---
INDEX_DIR = "indexes/my_lucene_index"
PDF_FOLDER = "pdf_corpus"

# Page Setup
st.set_page_config(page_title="My PDF Search Engine", layout="centered")
st.title("PDF Search Engine")
st.markdown("Search through the corpus and download documents. This corpus was built using ArXiv papers on machine learning.")

# --- LOAD SEARCHER (Cached for speed) ---
# We use @st.cache_resource so it doesn't reload the index every time you type
@st.cache_resource
def load_searcher():
    if not os.path.exists(INDEX_DIR):
        return None
    return LuceneSearcher(INDEX_DIR)

searcher = load_searcher()

# --- THE SEARCH UI ---
query = st.text_input("Enter your search term:", placeholder="e.g., machine learning")

if query:
    if searcher is None:
        st.error(f"Index not found at {INDEX_DIR}. Did you run index.py?")
    else:
        # Run the search
        hits = searcher.search(query, k=102) # Getall results (up to 100)
        
        st.subheader(f"Found {len(hits)} results for '{query}':")
        
        if len(hits) == 0:
            st.warning("No documents found.")
        
        # Display Results
        for i, hit in enumerate(hits):
            filename = hit.docid
            score = hit.score
            file_path = os.path.join(PDF_FOLDER, filename)
            
            # Create a nice card for each result
            with st.container():
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**{i+1}. {filename}**")
                    st.caption(f"Relevance Score: {score:.4f}")
                
                with col2:
                    # THE DOWNLOAD BUTTON LOGIC
                    if os.path.exists(file_path):
                        with open(file_path, "rb") as pdf_file:
                            st.download_button(
                                label="⬇ Download",
                                data=pdf_file,
                                file_name=filename,
                                mime="application/pdf",
                                key=f"btn_{i}" # Unique ID for each button
                            )
                    else:
                        st.error("File missing")
            
            st.divider() # Adds a horizontal line between results