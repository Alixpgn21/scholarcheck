# ScholarCheck Test Suite

Suite complète de tests pour ScholarCheck - Vérification de références bibliographiques et génération de sections "Related Work".

## Structure

```
tests/
├── README.md                           (ce fichier)
├── reference_checker/
│   ├── README.md                       (Pièges et guide d'interprétation)
│   ├── documents/
│   │   ├── test_1_basic_correct.tex    (Références valides simples)
│   │   ├── test_2_hallucinations.tex   (Fabrications complètes)
│   │   ├── test_3_metadata_errors.md   (Erreurs année/auteurs)
│   │   ├── test_4_semantic_traps.docx  (Contradictions NLI)
│   │   ├── test_5_mixed_cases.tex      (Mélange ok/error)
│   │   ├── test_6_edge_cases.md        (Cas limites)
│   │   └── test_7_comprehensive.tex    (29+ références, tous types)
│   └── expected_results/
│       └── results_guide.md            (Résultats attendus expliqués)
│
└── related_work_generator/
    ├── README.md                       (Pièges et guide d'interprétation)
    ├── corpus/
    │   ├── corpus_1_rag_basics/        (5 papiers sur RAG)
    │   ├── corpus_2_nlp_diversity/     (10 papiers NLP hétérogènes)
    │   ├── corpus_3_conflicting/       (Papiers avec avis opposés)
    │   ├── corpus_4_minimal/           (Docs sans abstracts)
    │   └── corpus_5_comprehensive/     (50+ papiers multi-domaines)
    ├── topics.txt                      (Topics à tester)
    └── expected_results/
        └── generation_guide.md         (Résultats attendus expliqués)
```

## Comment utiliser

### Reference Checker Tests

1. **Accéder à l'interface** : http://localhost:8000 → Tab 1
2. **Upload chaque document** depuis `reference_checker/documents/`
3. **Comparer avec** `reference_checker/expected_results/results_guide.md`

### Related Work Generator Tests

1. **Accéder à l'interface** : http://localhost:8000 → Tab 2
2. **Upload corpus** depuis `related_work_generator/corpus/`
3. **Utiliser topic** de `topics.txt`
4. **Comparer résultat avec** `related_work_generator/expected_results/generation_guide.md`

## Pièges couverts

### Reference Checker
- ✅ Hallucinations complètes (DOI fake, journal inexistant)
- ✅ Métadonnées erronées (année, auteurs)
- ✅ Contradictions sémantiques (phrase vs abstract)
- ✅ DOI formats variés (arXiv, Nature, CrossRef)
- ✅ Noms d'auteurs composés (Pouget-Abadie)
- ✅ Références partiellement correctes
- ✅ Cas limites (année ancienne, 1 auteur)

### Related Work Generator
- ✅ Clustering automatique par thème
- ✅ Hallucinations évitées via RAG
- ✅ Self-Refine loop validation
- ✅ Corpus avec peu d'abstracts
- ✅ Papiers avec avis opposés
- ✅ Diversité multi-domaines
- ✅ Topics ambigus vs spécifiques

---

**Version**: 1.0  
**Last updated**: 2025-05-22  
**Testing framework**: Automated + Manual validation
