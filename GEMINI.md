# Explication du Projet ScholarCheck

## 🎯 Quel est le but du projet ?
ScholarCheck est un outil SaaS de R&D conçu pour le monde académique. Son rôle principal est de **lutter contre les hallucinations des intelligences artificielles (LLMs)** dans les publications scientifiques.

Très souvent, les modèles de langage génératifs inventent de faux articles de recherche ou citent de vrais articles pour appuyer des propos qui n'y figurent pas. ScholarCheck aide les chercheurs à sécuriser leur travail en permettant de :
1. **Auditer un manuscrit complet** pour vérifier si toutes les références citées existent réellement et si elles soutiennent bien le propos du texte.
2. **Générer une section "État de l'art" (Related Work)** de haute fiabilité, où chaque phrase rédigée est rigoureusement rattachée à un document véritable préalablement validé.

---

## ⚙️ Comment ça marche ? (Les 2 modules clés)

### 1. Le Vérificateur de Références (Reference Checker)
Lorsque vous uploadez un document (LaTeX, Word, ou Markdown), l'outil va :
- **Extraire** toutes les citations détectées dans votre texte.
- **Interroger** en temps réel trois bases de données de recherche mondiales (CrossRef, OpenAlex, Semantic Scholar) pour valider l'existence du DOI, des auteurs, et de l'année.
- **L'innovation (Vérification Sémantique) :** L'outil convertit la phrase où vous citez l'article et le résumé officiel (abstract) de l'article en valeurs mathématiques (Embeddings). Il calcule ensuite la "distance" entre les deux. Si le score est trop bas, le système vous avertit que vous faites potentiellement dire à la source quelque chose qu'elle ne dit pas (hallucination sémantique).

### 2. Le Générateur d'État de l'Art (Related Work)
Vous fournissez une liste de DOIs ou un corpus de fichiers. L'outil va :
- **Vectoriser** les documents (via le modèle NLP `MiniLM`).
- **Classifier** automatiquement les articles qui parlent des mêmes thématiques grâce à un algorithme d'apprentissage non supervisé (`KMeans Clustering`).
- **Rédiger (Architecture RAG) :** Il fournit au modèle de langage (Claude d'Anthropic) les meilleurs représentants de chaque groupe thématique pour lui demander de rédiger un texte structuré, avec pour obligation stricte de se baser uniquement sur ce contexte fourni.

---

## 🛠️ Stack Technique & Architecture
- **Backend :** API Python robuste construite avec le framework **FastAPI** (Uvicorn pour le serveur local).
- **Frontend :** Interface web légère en **Vanilla JS** (HTML/CSS/JS classiques) afin de rester rapide et simple, communiquant avec l'API.
- **Traitement de Données (Data Science) :** Utilisation de `scikit-learn` pour le clustering et `sentence-transformers` pour la création des embeddings sémantiques.

---

## 🚀 Roadmap R&D (Next Steps)

Afin de pousser ce prototype vers l'état de l'art académique, les améliorations suivantes sont planifiées :
1. **Inférence Logique (NLI)** : Remplacer la Similarité Cosinus par un Cross-Encoder pour détecter la contradiction sémantique stricte.
2. **Caching & DB Locale** : Système de mise en cache SQLite pour optimiser les requêtes aux APIs (CrossRef, OpenAlex).
3. **Self-Refine (RAG)** : Boucle d'auto-évaluation par le LLM pour certifier 100% de fiabilité sur la section générée.
4. **Graph RAG & Full-Text** : Intégration du réseau de citations croisées (OpenAlex) pour affiner le clustering.

Commit a chaque fois pour garder une trace de la progression et gérer les versions.