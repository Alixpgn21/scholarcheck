# ScholarCheck

SaaS de vérification bibliographique et de génération de section Related Work.

## Lancer le projet

### 1. Cloner et configurer les variables d'environnement

```bash
cp .env.example .env
# Remplir ANTHROPIC_API_KEY dans .env
```

### 2. Installer les dépendances Python

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Démarrer le serveur

```bash
cd backend
uvicorn main:app --reload --port 8000
```

Le frontend est servi automatiquement sur http://localhost:8000

La doc API interactive est sur http://localhost:8000/docs

---

## Architecture

```
scholarcheck/
├── backend/
│   ├── main.py                          # FastAPI app + routing
│   ├── config.py                        # Variables d'environnement
│   ├── requirements.txt
│   ├── modules/
│   │   ├── parser.py                    # Parsing LaTeX / docx / Markdown
│   │   ├── reference_checker/
│   │   │   ├── api_client.py            # CrossRef, OpenAlex, Semantic Scholar
│   │   │   ├── verifier.py              # Vérification + consolidation
│   │   │   └── semantic.py              # Similarité cosinus phrase ↔ abstract
│   │   └── related_work/
│   │       ├── embeddings.py            # SentenceTransformer embeddings
│   │       ├── clustering.py            # KMeans + silhouette score auto
│   │       └── generator.py            # RAG → Claude (génération Related Work)
│   └── routers/
│       ├── checker.py                   # POST /checker/upload
│       └── related_work.py             # POST /related-work/generate
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
└── uploads/                            # Fichiers uploadés (auto-créé)
```

## Endpoints API

### Module 1 — Vérificateur de références

| Méthode | Route | Description |
|---------|-------|-------------|
| POST | `/checker/upload` | Upload manuscrit → rapport complet |
| POST | `/checker/verify-doi` | Vérification d'un DOI unique |

### Module 2 — Générateur Related Work

| Méthode | Route | Description |
|---------|-------|-------------|
| POST | `/related-work/generate` | Upload corpus de fichiers |
| POST | `/related-work/generate-from-dois` | Liste de DOIs en JSON |

## Sources académiques utilisées

- **CrossRef** — vérification DOI, métadonnées officielles (gratuit)
- **OpenAlex** — base ouverte 250M+ articles (gratuit)
- **Semantic Scholar** — abstracts, embeddings sémantiques (gratuit avec clé)

## Pipeline de détection des hallucinations

```
Manuscrit → Extraction citations → Requête APIs (3 sources) → 
Vérification DOI/auteurs/année → Similarité sémantique phrase↔abstract → Rapport
```

## Pipeline Related Work

```
Corpus → Embeddings (MiniLM) → Clustering KMeans auto-k → 
Représentants par cluster → Prompt RAG → Claude → Section structurée
```

## 🚀 Roadmap R&D (Next Steps)

Afin de pousser ce prototype vers l'état de l'art académique, les améliorations suivantes sont planifiées :
1. **Inférence Logique (NLI)** : Remplacer la Similarité Cosinus par un Cross-Encoder pour détecter la contradiction sémantique stricte.
2. **Caching & DB Locale** : Système de mise en cache SQLite pour optimiser les requêtes aux APIs (CrossRef, OpenAlex).
3. **Self-Refine (RAG)** : Boucle d'auto-évaluation par le LLM pour certifier 100% de fiabilité sur la section générée.
4. **Graph RAG & Full-Text** : Intégration du réseau de citations croisées (OpenAlex) pour affiner le clustering.
