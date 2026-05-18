# État de l'art — ScholarCheck
## SaaS d'audit bibliographique et de génération de Related Work assistée par IA

**Projet R&D — Axe B**  
**Référent : Amine HADIR**  
**Durée : 2 semaines**

---

## Table des matières

1. [Introduction](#1-introduction)
2. [Hallucinations bibliographiques dans les LLMs](#2-hallucinations-bibliographiques-dans-les-llms)
3. [Architecture RAG (Retrieval-Augmented Generation)](#3-architecture-rag-retrieval-augmented-generation)
4. [APIs et bases de données académiques](#4-apis-et-bases-de-données-académiques)
5. [Clustering de documents scientifiques par embeddings](#5-clustering-de-documents-scientifiques-par-embeddings)
6. [Synthèse et positionnement de ScholarCheck](#6-synthèse-et-positionnement-de-scholarcheck)
7. [Références bibliographiques](#7-références-bibliographiques)

---

## 1. Introduction

L'avènement des grands modèles de langage (LLMs — *Large Language Models*) a profondément modifié les pratiques de rédaction scientifique. Des outils comme ChatGPT, Claude ou Gemini sont désormais utilisés par des chercheurs pour accélérer la production de textes académiques, notamment les sections de revue de littérature (*related work*) et les introductions. Cette adoption rapide s'accompagne cependant d'un risque majeur, identifié par la communauté scientifique dès 2023 : la **fabrication de références bibliographiques inexistantes**, communément appelée *hallucination bibliographique*.

Ce phénomène n'est pas anecdotique. Plusieurs articles publiés dans des revues à comité de lecture ont été rétractés ou corrigés après la découverte de citations vers des papiers qui n'existent pas — avec de faux auteurs, de faux titres, de faux DOIs. Au-delà du cas extrême de la rétractation, un problème plus subtil et plus répandu consiste en des **citations techniquement réelles mais sémantiquement inadéquates** : le papier cité existe, mais son contenu ne soutient pas l'affirmation pour laquelle il est invoqué.

Le projet **ScholarCheck** vise à répondre à ces deux problèmes en construisant un SaaS capable (1) d'auditer un manuscrit pour détecter les références défaillantes, et (2) d'assister la rédaction de sections *related work* où chaque affirmation est ancrée sur des sources réellement consultées. Cet état de l'art examine les travaux existants sur les quatre axes technologiques qui fondent ce système.

---

## 2. Hallucinations bibliographiques dans les LLMs

### 2.1 Définition et taxonomie des hallucinations

Le terme *hallucination* dans le contexte des LLMs désigne la génération de texte fluide et cohérent en apparence, mais factuellement incorrect ou non fondé. Ji et al. [1] proposent une taxonomie complète dans leur survey de 2023, distinguant les hallucinations **intrinsèques** (contradictions avec la source fournie) des hallucinations **extrinsèques** (affirmations non vérifiables ou fausses par rapport au monde réel).

Dans le domaine scientifique, Maynez et al. [2] ont été parmi les premiers à mesurer quantitativement ce phénomène dans le cadre du résumé automatique, montrant que même des modèles performants génèrent des affirmations factuellement non soutenues par le document source. Leurs résultats indiquent que jusqu'à 70 % des résumés générés contiennent au moins une forme d'hallucination.

### 2.2 Hallucinations spécifiques aux citations bibliographiques

Les hallucinations bibliographiques constituent une sous-catégorie particulièrement problématique car elles sont difficiles à détecter sans consultation des sources primaires, et leurs conséquences sur l'intégrité scientifique sont directes.

**Nature des fabrications.** Walters et Wilder [3] ont conduit une des premières études empiriques systématiques sur ce phénomène avec ChatGPT (GPT-3.5). Ils ont soumis au modèle des demandes de génération de bibliographies sur des sujets académiques précis, puis vérifié chaque référence produite. Leurs résultats sont frappants : une proportion significative des références générées étaient entièrement fictives — titres plausibles, auteurs plausibles (parfois réels mais n'ayant pas écrit le papier cité), années cohérentes, journaux existants, mais articles inexistants. Les DOIs générés étaient soit invalides, soit pointaient vers des articles différents.

**Cas réels de rétractation.** Plusieurs cas documentés montrent les conséquences concrètes. Des avocats américains ont été sanctionnés en 2023 pour avoir soumis des mémoires juridiques contenant des citations générées par ChatGPT — des affaires judiciaires entièrement inventées avec des noms de parties, dates et numéros de dossier fabriqués. Dans le domaine médical, Athaluri et al. [4] ont publié une étude dans *Cureus* examinant spécifiquement ce phénomène pour l'écriture scientifique biomédicale, confirmant la fréquence élevée des citations non vérifiables.

### 2.3 Causes mécanistiques

Comprendre pourquoi les LLMs hallucinent des références éclaire la conception des solutions.

**Mémorisation imparfaite.** Les LLMs sont entraînés sur des corpus massifs incluant de nombreux articles scientifiques. Ils mémorisent des *patterns* de citation (structure auteur-année-titre-journal) et des associations entre auteurs et domaines, mais pas les articles eux-mêmes dans leur intégralité. Lors de la génération, le modèle produit des structures de citation syntaxiquement valides en interpolant entre les patterns mémorisés, ce qui donne des références qui *ressemblent* à de vraies références sans l'être.

**Absence de mécanisme de vérification interne.** Contrairement à un humain qui consulte une base de données avant de citer, un LLM génère token par token de manière autoregressive sans accès à une source externe de vérité. La plausibilité stylistique est récompensée lors de l'entraînement, pas la factualité bibliographique.

**Coupure temporelle (cutoff).** Les LLMs ont une date de coupure de leurs données d'entraînement. Toute demande portant sur des publications récentes augmente le risque d'hallucination, car le modèle doit extrapoler au-delà de ce qu'il a vu.

### 2.4 Métriques d'évaluation

Plusieurs métriques ont été proposées pour évaluer la factualité des LLMs :

- **BERTScore** [5] : mesure la similarité sémantique entre le texte généré et une référence via des embeddings BERT, mais ne vérifie pas la factualité externe.
- **FactScore** [6] : décompose les affirmations d'un texte en faits atomiques et vérifie chacun contre une base de connaissances. Applicable aux citations si la base inclut des métadonnées bibliographiques.
- **Vérification par API** (approche de ScholarCheck) : interrogation directe de bases bibliographiques pour confirmer l'existence des références citées — approche plus fiable car elle consulte des sources primaires.

---

## 3. Architecture RAG (Retrieval-Augmented Generation)

### 3.1 Principes fondamentaux

Le **Retrieval-Augmented Generation** (RAG) est une architecture hybride proposée par Lewis et al. [7] dans leur papier séminal de NeurIPS 2020. L'idée centrale est de découpler la mémoire paramétrique du LLM (ce qu'il a mémorisé lors de l'entraînement) de la mémoire non-paramétrique (une base de documents interrogeable à la volée).

Le pipeline RAG standard se décompose en trois phases :

```
Query → [Retriever] → Documents pertinents → [Generator (LLM)] → Réponse ancrée
                ↑
         Base vectorielle
```

1. **Indexation** : les documents du corpus sont encodés en vecteurs denses (embeddings) et stockés dans un index vectoriel.
2. **Retrieval** : à la réception d'une requête, le retriever calcule la similarité entre la requête encodée et les documents indexés, et retourne les k plus proches voisins.
3. **Génération** : le LLM reçoit en contexte la requête originale *et* les documents récupérés, ce qui l'ancre sur du contenu réel pour sa génération.

### 3.2 Composants du retrieval

**Dense Passage Retrieval (DPR).** Karpukhin et al. [8] ont introduit DPR, une approche où deux encodeurs BERT distincts encodent respectivement les questions et les passages, entraînés conjointement par contraste. DPR surpasse les méthodes sparse traditionnelles (TF-IDF, BM25) sur les benchmarks de question-answering en domaine ouvert.

**Sentence-BERT.** Reimers et Gurevych [9] ont développé Sentence-BERT (SBERT), une adaptation de BERT utilisant une architecture siamoise pour produire des embeddings de phrases sémantiquement comparables via similarité cosinus. SBERT est devenu le backbone standard des retrievers dans les systèmes RAG légers, notamment via la librairie `sentence-transformers`. ScholarCheck utilise le modèle `all-MiniLM-L6-v2`, une distillation de SBERT optimisée pour la vitesse sur CPU.

**ColBERT.** Khattab et Zaharia [10] proposent ColBERT (*Contextualized Late Interaction over BERT*), une architecture qui retarde l'interaction entre la requête et le document au moment du scoring, permettant un retrieval plus précis tout en maintenant une efficacité computationnelle acceptable.

### 3.3 RAG appliqué à l'écriture scientifique

**SPECTER.** Cohan et al. [11] ont entraîné SPECTER (*Scientific Paper Embeddings using Citation-informed TransformERs*), un modèle spécialisé pour l'encodage de papiers scientifiques. Contrairement à BERT généraliste, SPECTER exploite la structure des citations lors de l'entraînement (les papiers cités ensemble tendent à être proches dans l'espace vectoriel), ce qui produit des embeddings particulièrement adaptés aux tâches de retrieval scientifique.

**S2ORC.** Lo et al. [12] ont publié le Semantic Scholar Open Research Corpus (S2ORC), un corpus massif de 81,1 millions de papiers scientifiques avec métadonnées structurées, texte intégral parsé et graphe de citations. S2ORC constitue l'infrastructure sous-jacente à l'API Semantic Scholar utilisée dans ScholarCheck.

**Limitations du RAG pour la vérification bibliographique.** Le RAG standard résout le problème de la génération — il ancre le texte produit sur des sources réelles. Il ne résout pas directement le problème de *vérification* d'un manuscrit existant, où les citations sont déjà présentes et où la tâche est de les valider a posteriori. C'est pourquoi ScholarCheck combine deux approches : vérification par API (pour l'audit) et RAG (pour la génération de *related work*).

### 3.4 Évolutions récentes : RAG avancé

**Self-RAG.** Asai et al. [13] proposent une approche où le LLM apprend lui-même à décider quand effectuer un retrieval, et à évaluer la pertinence et la supportabilité des passages récupérés via des tokens de réflexion spéciaux. Cette approche améliore la précision factuelle sans dégrader la fluidité.

**CRAG (Corrective RAG).** Yan et al. [14] introduisent un mécanisme correctif qui évalue la qualité du retrieval et déclenche des stratégies alternatives (reformulation de requête, recherche web) si les documents récupérés sont jugés insuffisants — directement applicable au contexte de vérification bibliographique.

---

## 4. APIs et bases de données académiques

### 4.1 CrossRef

**Présentation.** CrossRef est un organisme à but non lucratif fondé en 2000 par un consortium d'éditeurs académiques. Il maintient la base de référence pour l'enregistrement des DOIs (*Digital Object Identifiers*) dans le domaine académique, couvrant plus de 150 millions de métadonnées de publications.

**API.** L'API REST CrossRef (`api.crossref.org`) est publiquement accessible sans clé d'authentification. Elle supporte la recherche par titre, auteur, DOI, ISSN, et retourne des métadonnées structurées en JSON incluant : DOI, titre, auteurs (nom de famille + prénom), date de publication, journal, volume, pages, URL, et parfois abstract.

**Polite pool.** CrossRef distingue deux pools de requêtes : le pool anonyme (limité, moins priorisé) et le *polite pool* (prioritaire, accès aux logs) accessible en fournissant simplement une adresse email via le paramètre `mailto`. ScholarCheck utilise cette pratique recommandée.

**Forces et limites.**

| Critère | Évaluation |
|---|---|
| Couverture | Très large (STM + SHS) |
| Fiabilité des métadonnées | Très haute (source primaire pour les DOIs) |
| Abstracts | Partiels (dépend de l'éditeur) |
| Accès texte intégral | Non |
| Mise à jour | En temps réel |
| Coût | Gratuit |

### 4.2 OpenAlex

**Présentation.** OpenAlex [15] est un index bibliographique entièrement open-source lancé en 2022 par OurResearch en remplacement de Microsoft Academic Graph (MAG). Il couvre plus de 240 millions d'œuvres scientifiques avec un accent fort sur l'open access et la réutilisabilité des données.

**Particularités techniques.** OpenAlex propose une reconstruction des abstracts via un *inverted index* — une structure qui stocke la position de chaque mot dans l'abstract plutôt que le texte brut, permettant une reconstruction fidèle tout en contournant certaines restrictions de copyright. ScholarCheck implémente cette reconstruction dans `api_client.py`.

OpenAlex structure ses données autour de cinq entités : Works, Authors, Institutions, Venues, Concepts — avec des identifiants stables (`openalex.org/W...`) et une API GraphQL-like supportant les filtres et les joins.

**Forces et limites.**

| Critère | Évaluation |
|---|---|
| Couverture | Très large (240M+) |
| Open access | Données entièrement libres (CC0) |
| Abstracts | Large couverture via inverted index |
| Concepts/Topics | Classification automatique par domaine |
| Graphe de citations | Oui |
| Coût | Gratuit |

### 4.3 Semantic Scholar

**Présentation.** Semantic Scholar est développé par l'Allen Institute for AI (AI2) depuis 2015. Sa particularité est d'être construit dès l'origine autour de l'IA : les métadonnées sont enrichies par des modèles NLP (extraction d'entités, détection de méthodes, extraction de résultats), et les papiers sont encodés via SPECTER pour permettre des recherches sémantiques.

**API Graph.** L'API Semantic Scholar (`api.semanticscholar.org/graph/v1`) supporte la recherche par titre, DOI, ArXiv ID, et retourne des champs sélectionnables : titre, auteurs, année, abstract, nombre de citations, références, champs d'étude. Une clé API optionnelle permet d'augmenter les rate limits.

**TLDR.** Semantic Scholar génère automatiquement un résumé d'une phrase par papier (*TLDR — Too Long; Didn't Read*) via un modèle seq2seq, accessible via l'API. Cette fonctionnalité est utile pour des comparaisons sémantiques rapides.

**Forces et limites.**

| Critère | Évaluation |
|---|---|
| Couverture | 200M+ papiers |
| Enrichissement IA | Très fort (méthodes, résultats, entités) |
| Abstracts | Très bonne couverture |
| Recherche sémantique | Native (SPECTER) |
| Graphe de citations | Très riche |
| Coût | Gratuit (rate limits) |

### 4.4 Comparaison synthétique

| Critère | CrossRef | OpenAlex | Semantic Scholar |
|---|---|---|---|
| Autorité sur les DOIs | ✅ Source primaire | Dérivé | Dérivé |
| Couverture | 150M | 240M | 200M |
| Abstracts | Partiel | Large | Large |
| Enrichissement IA | ❌ | Concepts auto | ✅ Fort |
| Open data | Partiel | ✅ CC0 | Partiel |
| Recherche sémantique | ❌ | Limité | ✅ Native |
| Rate limits | Généreux | Généreux | Modéré sans clé |

**Stratégie de ScholarCheck.** Le système interroge les trois APIs en parallèle (`asyncio.gather`) et applique une politique de priorité : CrossRef est la référence pour l'existence du DOI (source d'autorité), OpenAlex pour la reconstruction d'abstract, Semantic Scholar pour l'enrichissement sémantique. La convergence de plusieurs sources augmente le score de confiance.

---

## 5. Clustering de documents scientifiques par embeddings

### 5.1 Représentation vectorielle de textes scientifiques

**Du bag-of-words aux embeddings denses.** Les approches classiques de représentation documentaire (TF-IDF, BM25) produisent des vecteurs creux (*sparse*) de dimension égale à la taille du vocabulaire. Ces représentations ignorent la sémantique : "neural network" et "deep learning" sont orthogonaux dans l'espace TF-IDF. Les embeddings denses (*dense embeddings*) produits par des transformers encodent la sémantique dans un espace continu de dimension fixe (typiquement 384 à 1536 dimensions).

**SBERT pour les documents courts.** Pour les titres et abstracts, `sentence-transformers` avec le modèle `all-MiniLM-L6-v2` [9] offre un excellent rapport qualité/vitesse. Ce modèle, entraîné par distillation sur des centaines de millions de paires de phrases, produit des embeddings de dimension 384 en quelques millisecondes par document sur CPU.

**SPECTER pour les papiers complets.** Pour des corpus de papiers scientifiques avec texte intégral, SPECTER [11] et son successeur SPECTER2 produisent des embeddings qui capturent la structure disciplinaire et les relations de citation, surpassant SBERT sur les benchmarks de classification et clustering scientifique.

### 5.2 Méthodes de clustering

**K-Means.** L'algorithme K-Means est l'approche de référence pour le clustering de vecteurs denses. Il minimise la variance intra-cluster (somme des distances euclidiennes au centroïde). Ses limites connues sont la nécessité de spécifier k a priori, la sensibilité à l'initialisation, et l'hypothèse de clusters sphériques.

ScholarCheck contourne le problème du choix de k en testant automatiquement k ∈ [2, min(8, n)] et en sélectionnant le k optimal via le **silhouette score** [16]. Le silhouette score s(i) d'un point i est défini comme :

```
s(i) = (b(i) - a(i)) / max(a(i), b(i))
```

où a(i) est la distance moyenne intra-cluster et b(i) la distance moyenne au cluster le plus proche. Un score proche de 1 indique un clustering bien défini ; proche de 0, un chevauchement entre clusters.

**HDBSCAN.** Campello et al. [17] proposent HDBSCAN (*Hierarchical Density-Based Spatial Clustering of Applications with Noise*), une évolution de DBSCAN qui ne requiert pas de spécifier k et gère naturellement le bruit (documents hors-cluster). HDBSCAN est particulièrement adapté aux corpus de papiers scientifiques où certains documents sont interdisciplinaires et ne s'intègrent pas naturellement dans un thème dominant.

**BERTopic.** Grootendorst [18] a développé BERTopic, un framework de modélisation thématique qui combine embeddings de transformers, réduction de dimensionnalité (UMAP), clustering (HDBSCAN) et extraction de termes représentatifs (c-TF-IDF). BERTopic produit des clusters interprétables avec des labels thématiques automatiques, ce qui correspond directement au besoin de ScholarCheck d'identifier des "grands axes" thématiques.

### 5.3 Réduction de dimensionnalité pré-clustering

Le clustering directement dans l'espace de haute dimension (384D) souffre du *curse of dimensionality* : les distances euclidiennes deviennent peu discriminantes. McInnes et al. [19] proposent **UMAP** (*Uniform Manifold Approximation and Projection*), qui préserve mieux la structure globale que t-SNE tout en étant plus rapide et applicable à de nouveaux points (transductive).

L'usage de UMAP avant K-Means ou HDBSCAN est devenu une pratique standard dans les pipelines de clustering de documents NLP, adoptée notamment par BERTopic.

### 5.4 Évaluation de la qualité du clustering

Au-delà du silhouette score (sans label de vérité terrain), plusieurs métriques supervisées permettent d'évaluer la qualité thématique des clusters lorsqu'une annotation est disponible :

- **NMI** (*Normalized Mutual Information*) : mesure la concordance entre les clusters produits et les catégories réelles.
- **ARI** (*Adjusted Rand Index*) : mesure l'accord en tenant compte du hasard.
- **Cohérence thématique** (*Topic Coherence*) : évalue la co-occurrence des termes les plus représentatifs d'un cluster dans les documents réels.

---

## 6. Synthèse et positionnement de ScholarCheck

### 6.1 Gap dans la littérature

Plusieurs outils et travaux adressent partiellement les problèmes couverts par ScholarCheck :

- **Elicit** et **Consensus** : moteurs de recherche sémantique sur la littérature scientifique, mais sans audit de citations existantes.
- **scite.ai** : plateforme qui analyse comment les papiers sont cités (en soutien, en contradiction, ou de manière neutre), mais ne vérifie pas l'existence des références dans un manuscrit soumis.
- **iThenticate / Turnitin** : détectent le plagiat, pas les hallucinations bibliographiques.

Aucun outil ne combine en un seul pipeline : (1) l'extraction de citations depuis un manuscrit, (2) la vérification multi-source de leur existence, (3) la vérification sémantique de leur adéquation avec le texte citant, et (4) la génération de *related work* ancrée sur un corpus utilisateur.

### 6.2 Architecture de ScholarCheck en regard de l'état de l'art

| Composant ScholarCheck | Technique | Référence |
|---|---|---|
| Parser LaTeX/docx/Markdown | Extraction règles + `pylatexenc` | — |
| Vérification existence | APIs CrossRef + OpenAlex + Semantic Scholar | [15] |
| Vérification sémantique | Similarité cosinus sur embeddings SBERT | [9] |
| Embeddings corpus | `all-MiniLM-L6-v2` (sentence-transformers) | [9] |
| Clustering thématique | K-Means + silhouette score automatique | [16] |
| Génération Related Work | Template-based / RAG + Ollama | [7] |

### 6.3 Limites et perspectives

**Limites actuelles :**
- La vérification sémantique par similarité cosinus est sensible aux reformulations : une phrase citante et son abstract peuvent être sémantiquement alignés sans que la phrase citante soit vraiment soutenue par le papier (le papier peut *mentionner* le concept sans en être la source principale).
- Le clustering K-Means suppose des clusters sphériques, ce qui est rarement le cas pour des corpus interdisciplinaires.
- Le générateur template-based produit un texte structuré mais moins fluide qu'une génération LLM.

**Perspectives :**
- Intégrer SPECTER2 pour les embeddings de corpus afin d'exploiter la structure de citation.
- Remplacer K-Means par BERTopic pour des clusters thématiques avec labels automatiques.
- Ajouter un module de détection de *citation bias* : vérifier si certains auteurs ou laboratoires sont surreprésentés sans justification thématique.
- Étendre la vérification sémantique avec une approche NLI (*Natural Language Inference*) — vérifier si l'abstract *entail* la phrase citante au sens logique, pas seulement cosinus.

---

## 7. Références bibliographiques

[1] Ji, Z., Lee, N., Frieske, R., Yu, T., Su, D., Xu, Y., Ishii, E., Bang, Y., Madotto, A., & Fung, P. (2023). Survey of Hallucination in Natural Language Generation. *ACM Computing Surveys*, 55(12), 1–38. https://doi.org/10.1145/3571730

[2] Maynez, J., Narayan, S., Bohnet, B., & McDonald, R. (2020). On Faithfulness and Factuality in Abstractive Summarization. In *Proceedings of ACL 2020* (pp. 1906–1919). https://doi.org/10.18653/v1/2020.acl-main.173

[3] Walters, W. H., & Wilder, E. I. (2023). Fabrication and errors in the bibliographic citations generated by ChatGPT. *Scientific Reports*, 13, 14045. https://doi.org/10.1038/s41598-023-41032-5

[4] Athaluri, S. A., Manthena, S. V., Kesapragada, V. S. R. K. M., Yarlagadda, V., Dave, T., & Duddumpudi, R. T. S. (2023). Exploring the Boundaries of Reality: Investigating the Phenomenon of Artificial Intelligence Hallucination in Scientific Writing Through ChatGPT References. *Cureus*, 15(4), e37432. https://doi.org/10.7759/cureus.37432

[5] Zhang, T., Kishore, V., Wu, F., Weinberger, K. Q., & Artzi, Y. (2020). BERTScore: Evaluating Text Generation with BERT. In *Proceedings of ICLR 2020*. https://arxiv.org/abs/1904.09675

[6] Min, S., Krishna, K., Lyu, X., Lewis, M., Yih, W.-T., Koh, P. W., Iyyer, M., Zettlemoyer, L., & Hajishirzi, H. (2023). FActScoring: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation. In *Proceedings of EMNLP 2023*. https://arxiv.org/abs/2305.14251

[7] Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Küttler, H., Lewis, M., Yih, W.-T., Rocktäschel, T., Riedel, S., & Kiela, D. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. In *Advances in NeurIPS 2020*. https://arxiv.org/abs/2005.11401

[8] Karpukhin, V., Oğuz, B., Min, S., Lewis, P., Wu, L., Edunov, S., Chen, D., & Yih, W.-T. (2020). Dense Passage Retrieval for Open-Domain Question Answering. In *Proceedings of EMNLP 2020* (pp. 6769–6781). https://doi.org/10.18653/v1/2020.emnlp-main.550

[9] Reimers, N., & Gurevych, I. (2019). Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks. In *Proceedings of EMNLP 2019* (pp. 3982–3992). https://doi.org/10.18653/v1/D19-1410

[10] Khattab, O., & Zaharia, M. (2020). ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT. In *Proceedings of SIGIR 2020* (pp. 39–48). https://doi.org/10.1145/3397271.3401075

[11] Cohan, A., Feldman, S., Beltagy, I., Downey, D., & Weld, D. S. (2020). SPECTER: Document-level Representation Learning using Citation-informed Transformers. In *Proceedings of ACL 2020* (pp. 2270–2282). https://doi.org/10.18653/v1/2020.acl-main.207

[12] Lo, K., Wang, L. L., Neumann, M., Kinney, R., & Weld, D. S. (2020). S2ORC: The Semantic Scholar Open Research Corpus. In *Proceedings of ACL 2020* (pp. 4969–4983). https://doi.org/10.18653/v1/2020.acl-main.447

[13] Asai, A., Wu, Z., Wang, Y., Sil, A., & Hajishirzi, H. (2024). Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection. In *Proceedings of ICLR 2024*. https://arxiv.org/abs/2310.11511

[14] Yan, S.-Q., Gu, J.-C., Zhu, Y., & Ling, Z.-H. (2024). Corrective Retrieval Augmented Generation. https://arxiv.org/abs/2401.15884

[15] Priem, J., Piwowar, H., & Orr, R. (2022). OpenAlex: A fully-open index of the world's research literature. https://arxiv.org/abs/2205.01833

[16] Rousseeuw, P. J. (1987). Silhouettes: A graphical aid to the interpretation and validation of cluster analysis. *Journal of Computational and Applied Mathematics*, 20, 53–65. https://doi.org/10.1016/0377-0427(87)90125-7

[17] Campello, R. J. G. B., Moulavi, D., & Sander, J. (2013). Density-Based Clustering Based on Hierarchical Density Estimates. In *Proceedings of PAKDD 2013* (pp. 160–172). https://doi.org/10.1007/978-3-642-37456-2_14

[18] Grootendorst, M. (2022). BERTopic: Neural topic modeling with a class-based TF-IDF procedure. https://arxiv.org/abs/2203.05794

[19] McInnes, L., Healy, J., & Melville, J. (2018). UMAP: Uniform Manifold Approximation and Projection for Dimension Reduction. https://arxiv.org/abs/1802.03426

---

*Document rédigé dans le cadre du projet ScholarCheck — Projet R&D Axe B.*
