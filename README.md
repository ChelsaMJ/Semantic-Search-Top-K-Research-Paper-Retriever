# HON

HON is a command-line semantic search tool for research papers. It extracts paper metadata from PDFs, generates Gemini embeddings, stores them in a FAISS index, and retrieves the most relevant papers for a natural-language query.

## Requirements

- Python 3.11 or newer
- A Google API key with access to Gemini embeddings
- A ZIP archive containing the source PDFs

## Setup

Create and activate a virtual environment, then install the dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Set the API key in the current PowerShell session:

```powershell
$env:GOOGLE_API_KEY = "your-google-api-key"
```

The application reads `GOOGLE_API_KEY` directly from the process environment. The `.env.example` file is provided as a template, but `.env` is not loaded automatically by the current scripts.

## Build the index

Place a PDF dataset at `dataset.zip`, or pass another ZIP path to `build_index.py` by calling its `main` function from Python. Then run:

```powershell
python build_index.py
```

The ingestion pipeline:

1. Extracts PDFs into `pdf_extracted/`.
2. Extracts titles, abstracts, keywords, full text, and years into `papers.json`.
3. Generates Gemini document embeddings.
4. Saves the FAISS index to `papers_index.faiss` and metadata to `papers_metadata.json`.

## Search papers

After the index has been built, start the interactive search prompt:

```powershell
python search.py
```

Enter a research query and the number of results to retrieve when prompted. Results are ranked using semantic similarity and recency weighting.

## Project files

- `build_index.py` - Runs PDF ingestion, embedding generation, and index creation.
- `search.py` - Provides the interactive command-line search interface.
- `pdf_extractor.py` - Extracts structured records from PDFs.
- `data_loader.py` - Cleans paper data and builds embedding documents.
- `embedding_generator.py` - Calls the Gemini embedding API.
- `vector_store.py` - Builds, saves, and loads the FAISS index.
- `retriever.py` - Performs ranked paper retrieval.
- `config.py` - Stores API, model, ranking, and output-path configuration.

## Troubleshooting

- `KeyError: 'GOOGLE_API_KEY'`: set the environment variable before running either script.
- Missing `papers_index.faiss` or `papers_metadata.json`: run `python build_index.py` first.
- No PDFs found: verify that the ZIP contains files ending in `.pdf`, including inside nested folders.
