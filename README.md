# Lucene-Based PDF Search Engine

A full-stack Information Retrieval system that indexes 100 academic papers (PDFs) using Apache Lucene and provides a search interface via Streamlit.

## Project Structure
- `index.py`: Builds the Lucene Inverted Index.
- `stats.py`: Inspects the index (TF/DF counts).
- `app.py`: Web Interface for searching and downloading.
- `pd_corpus`: Will contain the pdfs

## Quick Start

**Prerequisite:** Ensure Java 21 is installed and `JAVA_HOME` is set.

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Build the Index:**
   ```bash
   python index.py
   ```
3. **Run the Search App:**

   ```bash
   python -m streamlit run app.py

   python stats.py
   ```

---

# The Technical Report

**Title:** Development of a Lucene-Based Inverted Index for Academic Retrieval  
**Date:** December 11, 2025  

### 1. Executive Summary
This project implements a full-stack Information Retrieval (IR) system capable of indexing, analyzing, and retrieving documents from a corpus of 100 academic research papers. The core engine utilizes **Apache Lucene** (via Pyserini) with BM25 ranking, supported by a statistical analyzer and a Streamlit web interface for document retrieval.

### 2. System Architecture & Environment
The project was developed on an Intel-based macOS environment using a Python-Java bridge.
* **Languages:** Python 3.11, Java 21 (Eclipse Temurin).
* **Libraries:** `pyserini` (Indexing), `pypdf` (Extraction), `streamlit` (UI).
* **Ranking Algorithm:** Okapi BM25.

### 3. Implementation Pipeline
1.  **Corpus Acquisition:** 100 PDFs on "Machine Learning" were fetched via the ArXiv API.
2.  **Text Extraction & Cleaning:** A custom pipeline in `index.py` extracts raw text using `pypdf`, sanitizes it (removing null bytes/formatting errors), and converts it to JSONL format.
3.  **Indexing:** The JSONL data is ingested by the Lucene Indexer to generate Postings Lists.
4.  **Search & Retrieval:** A web frontend (`app.py`) allows users to query the index. Results show the filename and relevance score, with a direct download link to the local PDF.

### 4. Challenges & Solutions
* **Java Versioning:** The system initially failed due to macOS defaulting to Java 11. This was resolved by installing **Eclipse Temurin JDK 21** and manually forcing the `JAVA_HOME` path.
* **Dependency Conflicts:** A runtime crash caused by NumPy 2.0 was resolved by pinning the dependency to `numpy<2`.
* **Data Integrity:** Initial indexing attempts crashed due to "dirty" characters in PDFs. A `clean_text()` function was implemented to strip control characters before indexing.

### 5. Result Analysis
The system successfully indexed 96% of the corpus.
* **Ranking Scores:** The reported "Relevance Score" is calculated using **BM25**, an unbounded probabilistic metric. It is not a percentage (out of 100) but a relative weight based on Term Frequency (TF) and Inverse Document Frequency (IDF). A higher score indicates a stronger match relative to the rest of the collection.
* **Performance:** Search queries execute in milliseconds, validating the efficiency of the Inverted Index structure ($O(1)$ lookup) over linear scanning.

### 6. Conclusion
This project successfully fulfilled the objective of constructing a function al Inverted Index. By transforming raw binaries into a queryable Lucene index, the system demonstrates the fundamental mechanisms of Information Retrieval. The dual-interface approach verified the index's structural integrity (via `stats.py`) and practical utility (via `app.py`), resulting in a robust search engine for academic literature.