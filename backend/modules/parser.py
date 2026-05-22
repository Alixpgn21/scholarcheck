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

    # Extraire les clés de citation \cite{key1, key2}
    cite_keys = re.findall(r"\\cite(?:p|t|alt)?\{([^}]+)\}", content)
    keys = []
    for group in cite_keys:
        keys.extend([k.strip() for k in group.split(",")])

    # Extraire les blocs \bibitem
    bibitem_pattern = re.findall(
        r"\\bibitem\{([^}]+)\}(.+?)(?=\\bibitem|\n\n|$|\\end\{thebibliography\})", content, re.DOTALL
    )
    bibliography = {key: raw.strip() for key, raw in bibitem_pattern}

    # Préserver les citations dans le texte brut
    content_for_text = re.sub(r"\\cite(?:p|t|alt)?\{([^}]+)\}", lambda m: f"[{m.group(1)}]", content)
    
    # Supprimer la bibliographie du texte brut pour éviter les faux positifs
    content_for_text = re.sub(r"\\begin\{thebibliography\}.*?\\end\{thebibliography\}", "", content_for_text, flags=re.DOTALL)

    text = LatexNodes2Text().latex_to_text(content_for_text)

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

    # Fix 2: Extraire les références depuis les blocs "**Reference:**" et les DOIs
    bibliography = {}
    cite_keys = []

    # Chercher les blocs explicites: **Reference:** ... DOI: 10.xxx
    # ou **Reference:** Author (year). Title. Venue.
    ref_blocks = re.finditer(
        r"\*\*Reference:\*\*\s*(.+?)(?=\n\n|\n##|\n\*\*Reference|\Z)",
        content,
        re.DOTALL | re.IGNORECASE,
    )
    for i, m in enumerate(ref_blocks):
        raw = m.group(1).strip().replace("\n", " ")
        # Générer une clé lisible depuis auteur + année
        year_m = re.search(r"\b(1[5-9]\d{2}|20\d{2})\b", raw)
        year_str = year_m.group(1) if year_m else str(i)
        # Premier mot qui ressemble à un nom de famille
        name_m = re.match(r"([A-Z][a-zé\-]+)", raw)
        name_str = name_m.group(1) if name_m else f"ref{i}"
        key = f"{name_str}{year_str}"
        bibliography[key] = raw
        cite_keys.append(key)

    # Fallback: chercher les DOIs isolés dans le texte (lignes contenant seulement un DOI)
    if not cite_keys:
        doi_lines = re.findall(r"10\.\d{4,9}/[-._;()/:A-Z0-9a-z]+", content)
        for j, doi in enumerate(doi_lines):
            key = f"doi_{j}"
            bibliography[key] = doi
            cite_keys.append(key)

    # Garder aussi la détection inline classique si présente
    inline_refs = re.findall(r"\[[\w\s,;]+\]|\([\w\s,]+,\s*\d{4}\)", content)
    for ref in inline_refs:
        if ref not in cite_keys:
            bibliography[ref] = ref
            cite_keys.append(ref)

    return {
        "text": text,
        "cite_keys": list(dict.fromkeys(cite_keys)),  # dédoublonner en préservant l'ordre
        "bibliography": bibliography,
        "format": "markdown",
    }


def extract_citing_sentences(text: str, cite_key: str) -> list[str]:
    """Retourne les phrases qui contiennent une référence à cite_key, nettoyées des artefacts LaTeX."""
    sentences = re.split(r"(?<=[.!?])\s+", text)
    result = []
    for s in sentences:
        if cite_key not in s:
            continue
        # Fix 6 + Fix 5: Supprimer les artefacts de conversion LaTeX
        # §.§ Section titles, symboles §, commandes LaTeX résiduelles
        clean = re.sub(r"§[\s§.]*", "", s)
        clean = re.sub(r"\\[a-zA-Z]+\{[^}]*\}", "", clean)  # \cmd{...}
        clean = re.sub(r"\s{2,}", " ", clean).strip()
        # Fix 5: Supprimer les titres de section en tête de phrase
        # ex: "Contested Areas The vaccine..." → "The vaccine..."
        # Un bloc de mots Title-Cased suivi d'une phrase normale
        clean = re.sub(r"^(?:[A-Z][a-zA-Z]+\s+){1,5}(?=[A-Z][a-z])", "", clean).strip()
        # Ne garder que les phrases suffisamment longues (évite les headers seuls)
        if len(clean) > 20:
            result.append(clean)
    return result
