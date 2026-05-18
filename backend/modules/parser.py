"""
Parse LaTeX, docx et Markdown pour extraire le texte brut et les citations.
"""
import re
from pathlib import Path


def parse_file(file_path: str) -> dict:
    path = Path(file_path)
    suffix = path.suffix.lower()

    if suffix == ".tex":
        return parse_latex(path.read_text(encoding="utf-8"))
    elif suffix == ".docx":
        return parse_docx(str(path))
    elif suffix in (".md", ".markdown"):
        return parse_markdown(path.read_text(encoding="utf-8"))
    else:
        raise ValueError(f"Format non supporté : {suffix}")


def parse_latex(content: str) -> dict:
    from pylatexenc.latex2text import LatexNodes2Text

    text = LatexNodes2Text().latex_to_text(content)

    # Extraire les clés de citation \cite{key1, key2}
    cite_keys = re.findall(r"\\cite(?:p|t|alt)?\{([^}]+)\}", content)
    keys = []
    for group in cite_keys:
        keys.extend([k.strip() for k in group.split(",")])

    # Extraire les blocs \bibitem
    bibitem_pattern = re.findall(
        r"\\bibitem\{([^}]+)\}(.+?)(?=\\bibitem|\n\n|$)", content, re.DOTALL
    )
    bibliography = {key: raw.strip() for key, raw in bibitem_pattern}

    return {
        "text": text,
        "cite_keys": list(set(keys)),
        "bibliography": bibliography,
        "format": "latex",
    }


def parse_docx(file_path: str) -> dict:
    from docx import Document

    doc = Document(file_path)
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    text = "\n".join(paragraphs)

    # Détecte les patterns de citation courants : [1], [Smith 2020], (Smith, 2020)
    inline_refs = re.findall(r"\[[\w\s,;]+\]|\([\w\s,]+,\s*\d{4}\)", text)

    return {
        "text": text,
        "cite_keys": list(set(inline_refs)),
        "bibliography": {},
        "format": "docx",
    }


def parse_markdown(content: str) -> dict:
    import markdown
    from html.parser import HTMLParser

    class TextExtractor(HTMLParser):
        def __init__(self):
            super().__init__()
            self.text_parts = []

        def handle_data(self, data):
            self.text_parts.append(data)

        def get_text(self):
            return " ".join(self.text_parts)

    html = markdown.markdown(content)
    extractor = TextExtractor()
    extractor.feed(html)
    text = extractor.get_text()

    inline_refs = re.findall(r"\[[\w\s,;]+\]|\([\w\s,]+,\s*\d{4}\)", content)

    return {
        "text": text,
        "cite_keys": list(set(inline_refs)),
        "bibliography": {},
        "format": "markdown",
    }


def extract_citing_sentences(text: str, cite_key: str) -> list[str]:
    """Retourne les phrases qui contiennent une référence à cite_key."""
    sentences = re.split(r"(?<=[.!?])\s+", text)
    return [s for s in sentences if cite_key in s]
