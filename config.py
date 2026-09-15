import os


GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
EMBEDDING_MODEL = "gemini-embedding-001"
CANDIDATE_MULTIPLIER=5
RECENCY_WEIGHT=0.4
INDEX_PATH="papers_index.faiss"
METADATA_PATH="papers_metadata.json"

