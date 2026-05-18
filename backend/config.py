from dotenv import load_dotenv
import os

load_dotenv()

SEMANTIC_SCHOLAR_API_KEY = os.getenv("SEMANTIC_SCHOLAR_API_KEY", "")
CROSSREF_EMAIL = os.getenv("CROSSREF_EMAIL", "scholarcheck@example.com")

CROSSREF_BASE_URL = "https://api.crossref.org/works"
OPENALEX_BASE_URL = "https://api.openalex.org/works"
SEMANTIC_SCHOLAR_BASE_URL = "https://api.semanticscholar.org/graph/v1"

UPLOAD_DIR = "../uploads"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
