# Reference Checker Test Suite

Tests exhaustifs pour le module de vérification des références.

## Documents de test

### 1. test_1_basic_correct.tex
**Objectif** : Valider que les références correctes passent tous les filtres

**Pièges testés** :
- Références standard (Nature, arXiv, IEEE)
- DOIs formats variés
- Auteurs simples vs composés
- Années récentes vs anciennes

**Résultat attendu** :
- ✅ Score global: **100%**
- ✅ Toutes les références: **ok**
- ✅ Zéro warnings

---

### 2. test_2_hallucinations.tex
**Objectif** : Détecter les fabrications complètes

**Pièges testés** :
- **Smith 2024 - Quantum Teleportation** : Journal fictif + DOI fake
- **Johnson 2023 - Machine Consciousness** : Titre pseudo-scientifique impossible
- **Newton 1850 - Victorian AI** : Anachronisme + date avant ordinateurs
- **Thompson 2024 - Perpetual Motion** : Défie les lois physiques
- **Goldman 2023 - Aging Reversal** : Miracle medical inexistant

**Résultat attendu** :
- ✅ Score global: **0%** (toutes hallucinations)
- ✅ Toutes références: **not_found**
- ✅ Confiance: **0.0** partout
- ⚠️ Messages: "Aucune source n'a trouvé cette référence"

**Pourquoi** : Aucune API (CrossRef, OpenAlex, Semantic Scholar) n'indexe ces papiers inventés.

---

### 3. test_3_metadata_errors.md
**Objectif** : Détecter les erreurs de métadonnées

**Pièges testés** :
- **ResNet 2012 (au lieu de 2015)** : Année décalée de 3 ans
- **Attention Bahdanau 2010 (au lieu de 2014)** : Année incorrecte
- **Recommenders - Auteurs erronés** : Noms changés dans la citation

**Résultat attendu** :
- ✅ Score global: **40-60%** (référence trouvée mais métadonnées fausses)
- ⚠️ Status: **warning** (trouvée mais problème)
- ⚠️ Confiance: **0.27-0.47** (pénalité pour incohérence)
- ⚠️ Message: "Année incorrecte: trouvé 2015, attendu 2012"
- ⚠️ Ou: "Auteurs non trouvés: smith, jones"

**Pourquoi** : L'API résout le DOI vers le bon papier, mais les métadonnées locales ne match pas.

---

### 4. test_4_semantic_traps.docx
**Objectif** : Détecter les contradictions sémantiques via NLI

**Pièges testés** :
- **Vaccine Safety Contradiction** :
  - Phrase citante: "The vaccine was ineffective and caused severe reactions"
  - Abstract réel: "Efficacy and safety of mRNA-1273 vaccine"
  - NLI verdict: **CONTRADICTION** 🚨

- **Climate Denial** :
  - Phrase citante: "Climate change is caused by solar cycles"
  - Abstract réel: "Global patterns caused by human greenhouse gases"
  - NLI verdict: **CONTRADICTION** 🚨

- **GPT-4 as AGI** :
  - Phrase citante: "GPT-4 has achieved artificial general intelligence"
  - Abstract réel: "Large language model technical report"
  - NLI verdict: **CONTRADICTION** ou **AMBIGUOUS**

**Résultat attendu** :
- ✅ Status: **ok** (référence existe)
- 🚨 Badge NLI: **suspect** ou **ambigu**
- 🚨 Score NLI: **0.7-0.9** (contradiction score élevé)
- ℹ️ Raison: "Abstract contradicts the citing statement"

**Pourquoi** : La référence existe et le DOI résout, mais la **sémantique** est inversée. C'est une hallucination d'interprétation.

---

### 5. test_5_mixed_cases.tex
**Objectif** : Tester un mélange réaliste d'ok/warning/not_found

**Composition** :
- 5 références valides (ok)
- 3 avec métadonnées erronées (warning)
- 2 complètement fausses (not_found)
- 1 contradiction sémantique (suspect)

**Résultat attendu** :
- ✅ Score global: **50-60%**
- ✅ Breakdown:
  - ok: 5
  - warning: 3
  - not_found: 2
  - suspect: 1

---

### 6. test_6_edge_cases.md
**Objectif** : Tester les limites du système

**Pièges testés** :
- **Papier ultra-ancien** (1850) : Année très loin du présent
- **Papier futur** (2050) : Année impossible
- **Un seul auteur** : "Goodfellow, I."
- **Très many auteurs** : "Smith, J., Jones, K., Brown, M., ..."
- **Accents dans auteurs** : "Müller, Z.", "François, P."
- **DOI arXiv** : `10.48550/arXiv.XXXX` (souvent non indexé)
- **Sans DOI** : Référence par titre seulement
- **Titre très court** : "AI"
- **Titre très long** : 100+ caractères

**Résultat attendu** :
- ⚠️ Certains peuvent être **not_found** (limitations API, pas bug)
- ✅ Aucun crash ou erreur 500
- ⚠️ Handling gracieux des edge cases

**Pourquoi** : Les APIs ont des limitations. Par ex, arXiv DOIs ne sont pas toujours indexés.

---

### 7. test_7_comprehensive.tex
**Objectif** : Test complet avec 29+ références couvrant TOUS les cas

**Composition** :
- 13 références correctes
- 5 avec métadonnées erronées
- 11 complètement fausses
- 1 contradiction sémantique
- Multiple edge cases

**Résultat attendu** :
- ✅ Score global: **44-50%** (attendu sur dataset mixte)
- ✅ Détections correctes des hallucinations
- ✅ Temps total: <30 secondes

**Utilité** : Benchmark complet du système - le test de production.

---

## Comment interpréter les résultats

### Statuts possibles par référence

```
ok (vert) 
  → Référence trouvée, métadonnées match, pas de contradiction sémantique
  → Confiance: 0.5-1.0
  → Action: Aucune - tout va bien

warning (orange)
  → Référence trouvée mais problème détecté:
    * Année incorrecte (±1 an dépassé)
    * Auteurs ne matchent pas
    * Confiance réduite
  → Confiance: 0.27-0.47
  → Action: Vérifier manuellement la citation

not_found (rouge)
  → Aucune API n'a trouvé la référence
  → Confiance: 0.0
  → Cause possible:
    * Papier inventé (hallucination)
    * DOI arXiv non indexé (limitation API)
    * Titre trop vague ou mal orthographié
  → Action: Chercher manuellement ou retirer la citation

suspect (orange foncé)
  → Badge NLI additionnel
  → Référence trouvée MAIS sémantique contradictoire
  → Score NLI: 0.7-0.9 (contradiction dominante)
  → Action: Vérifier que la phrase citante interprète correctement
```

### Confiance score

```
1.0-0.8 = Très fiable (référence trouvée par 3 APIs, aucun problème)
0.8-0.5 = Fiable (trouvée par 2 APIs ou problème mineur)
0.5-0.27 = Problématique (trouvée mais métadonnées douteuses)
0.27-0.0 = Non fiable (pas trouvée ou grande contradiction)
```

### Hallucination Risk

```
Hallucination Risk = not_found + suspect_semantic

Risque élevé (>5) : Article nécessite audit avant publication
Risque moyen (2-5) : Vérifier les flaggées comme "not_found" ou "suspect"
Risque bas (<2) : Article probablement OK, mais lire les warnings
```

---

## Pièges courants et leur signification

### Piège 1: Référence trouvée mais année différente

**Scénario** :
- Citation dit: "Smith 1850"
- API retourne: DOI 10.1038/171737a0 → Watson & Crick 1953

**Verdict** : ⚠️ warning

**Interprétation** :
- Le DOI existe et résout vers un vrai papier
- MAIS l'année est complètement fausse (+103 ans !)
- C'est soit une erreur de typo, soit une corruption de la référence

**Action** :
- Vérifier si c'est le bon papier
- Si non, corriger le DOI ou l'année

---

### Piège 2: Papier valide mais phrase contradictoire

**Scénario** :
- Citation: "Vaccine was ineffective" (claiming inefficacy)
- Paper: "Efficacy and Safety of mRNA-1273 Vaccine" (claiming efficacy)

**Verdict** : ✅ ok + 🚨 suspect (NLI badge)

**Interprétation** :
- La référence EXISTE et VALIDE
- MAIS le chercheur interprète complètement à l'envers
- C'est UNE HALLUCINATION D'INTERPRETATION

**Action** :
- Lire le papier et corriger la phrase citante
- Ou retirer la citation si elle n'est vraiment pas supportée

---

### Piège 3: DOI arXiv non indexé

**Scénario** :
- Citation: DOI 10.48550/arXiv.1706.03762 (Attention is All You Need)
- Résultat: not_found

**Verdict** : ❌ not_found

**Interprétation** :
- Ce papier EXISTE (très célèbre) 
- MAIS son DOI arXiv n'est pas indexé dans CrossRef/OpenAlex/Semantic Scholar
- C'est une LIMITATION DE L'INDEX, pas une hallucination

**Action** :
- Chercher le papier manuellement
- Ou utiliser un titre search plutôt que DOI

---

### Piège 4: Auteurs avec tirets mal extraits

**Scénario** :
- Citation: "Pouget-Abadie, J., Warde-Farley, D."
- API retourne: "Goodfellow, I., Pouget-Abadie, J., Mirza, M., Xu, B., Warde-Farley, D."
- Extraction locale rate "Pouget-Abadie" → ne capture que "Abadie"

**Verdict** : ⚠️ warning "Auteurs non trouvés: abadie"

**Interprétation** :
- Le regex d'extraction des auteurs a loupé le tiret
- Les auteurs SONT dans l'API, c'est juste la détection locale qui bugge

**Action** :
- C'est une fausse alerte - le papier est correct
- Ignorez le warning (c'est un edge case connu)

---

## Résumé des pièges

| Piège | Document | Résultat attendu | Interprétation |
|-------|----------|------------------|----------------|
| Hallucination complète | test_2 | not_found | Papier inexistant |
| Année incorrecte | test_3 | warning | Métadonnée erronée |
| Auteurs incorrects | test_3 | warning | Métadonnée erronée |
| Contradiction sémantique | test_4 | ok + suspect | Mauvaise interprétation |
| DOI arXiv | test_6 | not_found | Limitation API |
| Auteurs composés | test_6 | ok ou warning | Edge case |
| Anachronisme | test_6 | not_found | Probablement hallucination |

---

**Interprétation Key** :
- ✅ ok = Tout va bien, confiance élevée
- ⚠️ warning = Quelque chose ne match pas, vérifier
- ❌ not_found = Papier introuvable ou hallucination
- 🚨 suspect = Sémantique contradictoire

**Ne pas confondre** :
- "not_found" ≠ toujours une hallucination (peut être limitation API)
- "ok" ≠ l'interprétation est correcte (voir badge NLI)
