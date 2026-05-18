from dotenv import load_dotenv
import os

load_dotenv()

SEMANTIC_SCHOLAR_API_KEY = os.getenv("SEMANTIC_SCHOLAR_API_KEY", "")
CROSSREF_EMAIL = os.getenv("CROSSREF_EMAIL", "scholarcheck@example.com")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

CROSSREF_BASE_URL = "https://api.crossref.org/works"
OPENALEX_BASE_URL = "https://api.openalex.org/works"
SEMANTIC_SCHOLAR_BASE_URL = "https://api.semanticscholar.org/graph/v1"

UPLOAD_DIR = "../uploads"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
NLI_MODEL = "cross-encoder/nli-distilroberta-base"
