#!/usr/bin/env python3
"""Génère l'état de l'art ScholarCheck en PDF via WeasyPrint."""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from weasyprint import HTML, CSS
from content import get_html_content, get_css

def main():
    output = os.path.join(os.path.dirname(__file__), "etat_de_lart_scholarcheck.pdf")
    html_content = get_html_content()
    css_content = get_css()
    HTML(string=html_content).write_pdf(output, stylesheets=[CSS(string=css_content)])
    print(f"PDF généré : {output}")

if __name__ == "__main__":
    main()
