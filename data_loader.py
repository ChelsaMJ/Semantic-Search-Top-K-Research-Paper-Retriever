import json
import re

# Loads dataset and builds single "document" string
def clean_text(text: str)-> str:
    if not text:
        return ""
    text=re.sub(r"\s+", " ", text)
    text=re.sub(r"[^\w\s.,;:()-]","",text)
    return text.strip().lower()

def load_papers(json_path: str)-> list[dict]:
    with open(json_path, "r", encoding="utf-8") as f:
        papers=json.load(f)
        
    for i, paper in enumerate(papers):
        paper["id"] =paper.get("id", i)
        paper["title"] =clean_text(paper.get("title", ""))
        paper["abstract"] =clean_text(paper.get("abstract", ""))
        paper["full_text"] =clean_text(paper.get("full_text", ""))
        keywords=paper.get("keywords", [])
        
        if isinstance(keywords, str):
            keywords=[k.strip() for k in keywords.split(",")]
        paper["keywords"]=[clean_text(k) for k in keywords]
        paper["year"]=int(paper.get("year",0))
        
    return papers

def build_document(paper: dict)->str:
    keyword_str=",".join(paper["keywords"])
    return f"Title: {paper['title']}, Keywords: {keyword_str}, Abstract:{paper['abstract']}"
        
        
        