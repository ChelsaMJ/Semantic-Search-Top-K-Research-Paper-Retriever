# Generate embeddings via gemini api

from google import genai
from google.genai import types
import numpy as np
import config

client=genai.Client(api_key=config.GOOGLE_API_KEY)

def get_embeddings(texts: list[str], model: str, batch_size: int =100)-> np.ndarray:
    all_embeddings=[]
    for i in range(0, len(texts),batch_size):
        batch=texts[i:i + batch_size]
        response =client.models.embed_content(
            model=model,
            contents=batch,
            config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT"),
        
        )
        all_embeddings.extend(e.values for e in response.embeddings)
    return np.array(all_embeddings,dtype="float32")

def get_query_embedding(query: str, model: str)->np.ndarray:
    response=client.models.embed_content(
        model=model,
        contents=[query],
        config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY"),
    )
    return np.array(response.embeddings[0].values, dtype="float32")






