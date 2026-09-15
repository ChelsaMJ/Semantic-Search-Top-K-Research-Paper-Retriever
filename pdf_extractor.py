# unzip dataset and extract structured field like title, abstract etc. from each paper
# produces papers.json file

import os
import re
import json
import zipfile
from pypdf import PdfReader

def unzip_pdfs(zip_path: str,extract_to: str = "pdf_extracted")->str:
    os.makedirs(extract_to, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(extract_to)
    return extract_to

def find_pdfs(folder: str) -> list[str]:
    #to handle nested odfs in subfolder after extraction
    pdf_paths=[]
    for root, _, files in os.walk(folder):
        for fname in files:
            if fname.lower().endswith(".pdf"):
                pdf_paths.append(os.path.join(root, fname))
    return sorted(pdf_paths)


def extract_year(text: str) ->int:
    matches=re.findall(r"\b(19|20)\d{2}\b", text)
    return int(matches[0]+text[text.find(matches[0])+ 2:text.find(matches[0])+4]) if False else(
        int(re.search(r"\b(19|20)\d{2}\b", text).group()) if re.search(r"\b(19|20)\d{2}\b", text) else 0
        
    )
    
def extract_title(first_page_text:str)-> str:
    lines=[l.strip() for l in first_page_text.split("\n") if l.strip()]
    ignored_prefixes = (
        "sciencedirect",
        "available online",
        "procedia computer science",
        "1877-",
        "this is an open access article",
        "peer-review under responsibility",
        "10.",
        "received:",
        "revised:",
        "accepted:",
        "published:",
        "citation:",
        "copyright:",
        "licensee",
        "https://",
        "www.",
        "29th international",
        "systems (kes",
        "see discussions",
        "article ",
        "article info",
    )
    in_citation = False
    for line in lines:
        if line.lower().startswith("citation:"):
            in_citation = True
            continue
        if in_citation and line.lower() == "article":
            in_citation = False
            continue
        if in_citation:
            continue
        if len(line) > 15 and not line.lower().startswith(ignored_prefixes):
            return line
    return lines[0] if lines else "unknown title"
    
def extract_abstract(first_page_text:str)-> str:
    match=re.search(r"abstract(.*?)(introduction|keywords|1\.\s)", first_page_text, re.IGNORECASE | re.DOTALL)

    if match:
        return match.group(1).strip()[:1500]
    return first_page_text[:800]

def extract_keywords(full_text: str)-> list[str]:
    match =re.search(r"keywords[:\s]*(.*?)(\n\n|introduction)", full_text, re.IGNORECASE | re.DOTALL)
    if match:
        raw=match.group(1)
        return [k.strip().lower() for k in re.split(r"[,;]", raw) if k.strip()][:10]
    return[]


def pdf_to_record(pdf_path:str, paper_id: int)-> dict:
    reader=PdfReader(pdf_path)
    first_page=reader.pages[0].extract_text() or ""
    full_text= " ".join((p.extract_text() or "") for p in reader.pages)
    
    return {
        "id": paper_id,
        "title": extract_title(first_page),
        "abstract": extract_abstract(first_page),
        "full text": full_text,
        "keywords": extract_keywords(full_text),
        "year": extract_year(first_page),
    }
    
def build_dataset_from_zip(zip_path: str, out_path: str="papers.json")-> str:
    extracted_folder=unzip_pdfs(zip_path)
    pdf_paths=find_pdfs(extracted_folder)
    print(f"Found {len(pdf_paths)} PDFs in {zip_path}")

    records=[]
    for i, path in enumerate(pdf_paths):
        try:
            records.append(pdf_to_record(path, i))
        except Exception as e:
            print(f"Skipped {os.path.basename(path)}: {e}")

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)
    print(f"Extracted {len(records)} papers to {out_path}")
    return out_path

if __name__=="__main__":
    build_dataset_from_zip("dataset.zip")
    
    





