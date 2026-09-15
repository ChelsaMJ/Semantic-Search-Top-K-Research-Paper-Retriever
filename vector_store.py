# build save and load faiss index

import faiss
import numpy as np
import json

def normalize(vectors: np.ndarray)->np.ndarray:
    norms =np.linalg.norm(vectors,axis=1,keepdims=True)
    norms[norms==0]=1e-10
    return vectors/norms

def build_index(embeddings: np.ndarray)-> faiss.Index:
    dim =embeddings.shape[1]
    index=faiss.IndexFlatIP(dim)
    index.add(normalize(embeddings))
    return index

def save_index(index: faiss.Index, papers: list[dict], index_path: str, metadata_path:str):
    faiss.write_index(index, index_path)
    with open(metadata_path,"w", encoding="utf-8") as f:
        json.dump(papers, f)
    
def load_index(index_path: str, metadata_path:str):
    index=faiss.read_index(index_path)
    with open(metadata_path,"r", encoding="utf-8") as f:
        papers=json.load(f)
    return index, papers
    
    
    
    
    
    
    
    
    
    
    
    