# full ingestion pipeline

from pdf_extractor import build_dataset_from_zip
from data_loader import load_papers, build_document
from embedding_generator import get_embeddings
from vector_store import build_index, save_index
import config

def main(zip_path: str = 'dataset.zip'):
    papers_json_path=build_dataset_from_zip(zip_path)
    papers=load_papers(papers_json_path)
    documents=[build_document(p) for p in papers]
    
    print(f"Embedding {len(documents)} papers...")
    embeddings=get_embeddings(documents, model=config.EMBEDDING_MODEL)
    
    index=build_index(embeddings)
    save_index(index, papers, config.INDEX_PATH, config.METADATA_PATH)
    print(f"Index built and saved to {config.INDEX_PATH} and {config.METADATA_PATH}")
    
if __name__=="__main__":
    main()