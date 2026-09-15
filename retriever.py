# retrieves the top-k most relevant paper for queries
# combines semantic similarity and recency

import numpy as np
from vector_store import normalize
from embedding_generator import get_query_embedding
import config

def min_max_normalize(values: np.ndarray)->np.ndarray:
    low, high = values.min(), values.max()
    if high-low< 1e-10:
        return np.ones_like(values)
    return (values-low)/(high-low)


def search(query: str, index, papers: list[dict], k: int,recency_weight: float=config.RECENCY_WEIGHT)-> list[dict]:
    query_vec=normalize(
        get_query_embedding(query, config.EMBEDDING_MODEL).reshape(1,-1)
    )
    
    candidate_k =min(k*config.CANDIDATE_MULTIPLIER, len(papers))
    similarities, indices =index.search(query_vec, candidate_k)
    similarities, indices=similarities[0], indices[0]
        
    candidates =[papers[i] for i in indices]
    years =np.array([c["year"] for c in candidates], dtype="float32")
    
    sim_norm=min_max_normalize(similarities)
    year_norm=min_max_normalize(years)
    combined_score = (1 -recency_weight)*sim_norm + recency_weight*year_norm
    
    top_idx=np.argsort(-combined_score)[:k]
    top_k=[candidates[i] for i in top_idx]
    
    
    # final output by recency, not combined score
    top_k.sort(key=lambda p: p["year"], reverse=True)
    return top_k
        
        
