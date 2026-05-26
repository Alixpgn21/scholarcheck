# Related Work Generator Test Suite

Comprehensive test suite for the Related Work Generator module, which uses RAG (Retrieval-Augmented Generation) to create "Related Work" sections from academic paper corpuses.

## Test Structure

```
related_work_generator/
├── README.md                    (this file)
├── corpus/
│   ├── corpus_1_rag_basics/     (5 papers on RAG core concepts)
│   ├── corpus_2_nlp_diversity/  (10 diverse NLP papers)
│   ├── corpus_3_conflicting/    (papers with opposing views)
│   ├── corpus_4_minimal/        (papers with missing/minimal abstracts)
│   └── corpus_5_comprehensive/  (50+ papers, all domains)
├── topics.txt                   (topics to test with each corpus)
└── expected_results/
    └── generation_guide.md      (expected outputs and interpretation)
```

## What Gets Tested

### 1. Corpus Quality Issues

**corpus_1_rag_basics** (5 papers)
- **Purpose**: Test RAG hallucination prevention (Self-Refine loop)
- **Pièges**:
  - Small corpus forces system to use every paper
  - All papers are directly relevant (no distractors)
  - Tests citation accuracy when corpus is focused
- **Expected outcome**: All papers cited with high accuracy
- **Test topic**: "retrieval-augmented generation for language models"

**corpus_2_nlp_diversity** (10 papers)
- **Purpose**: Test multi-theme clustering with diverse papers
- **Pièges**:
  - Papers span multiple NLP subdomains (NMT, embeddings, VQA, BERT, GPT)
  - Some papers not directly relevant to all topics
  - Tests thematic grouping and section organization
- **Expected outcome**: 2-4 coherent thematic sections
- **Test topics**: Multiple NLP topics

**corpus_3_conflicting** (3 papers with opposing views)
- **Purpose**: Test handling of conflicting viewpoints
- **Pièges**:
  - Paper 1 argues "scaling laws predict performance improvements"
  - Paper 2 argues "transformers have fundamental limitations"
  - Paper 3 argues "scaling has environmental/societal costs"
  - System must present all views without fabricating consensus
- **Expected outcome**: Sections acknowledge different perspectives
- **Test topic**: "scaling and limitations of language models"

**corpus_4_minimal** (papers with missing/empty abstracts)
- **Purpose**: Test robustness when abstracts are unavailable
- **Pièges**:
  - Paper 1: `abstract: null`
  - Paper 2: `abstract: ""` (empty string)
  - Paper 3: `abstract: "short sentence only"`
  - Minimal metadata tests how system handles missing information
- **Expected outcome**: System still generates coherent text (title + year used)
- **Test topic**: "neural network training and optimization"

**corpus_5_comprehensive** (50+ papers, all domains)
- **Purpose**: Production-level benchmark test
- **Pièges**:
  - Large corpus tests clustering performance
  - Diverse domains (NLP, Vision, RL, GNNs, Multimodal, Meta-learning, etc.)
  - Tests both precision (not including unrelated papers) and recall
  - Complex relationship graph requires good RAG clustering
- **Expected outcome**: 5-8 well-organized sections covering domains
- **Test topics**: Various specific and broad topics

### 2. RAG-Specific Pièges

**Hallucination Prevention (Self-Refine Loop)**
- Generated text should ONLY cite papers from corpus
- Every claim must be traceable to a paper abstract
- References to papers NOT in corpus should be REMOVED in refinement pass
- Test: Verify all paper titles mentioned are in the corpus

**Citation Format**
- Expected format: `[Paper Title]` from corpus
- Verify citations match exactly (case-sensitive)
- Test across different paper titles (long vs short)

**Semantic Clustering**
- Papers should be grouped by research theme
- Related papers grouped together
- Unrelated papers in separate sections
- Test: Manual inspection of section coherence

**Context Window Management**
- Large corpuses should not crash system
- Prompt should include representative samples, not full corpus
- Test: Performance with 50-paper corpus vs single topics

**Fallback Behavior**
- If LLM fails, template generation should still work
- No hallucinations in template mode (deterministic)
- Test: Disable all LLM APIs and verify output quality

## How to Test

### Step 1: Upload Corpus (Méthode A — fichiers .md)

```
1. Go to http://localhost:8000
2. Tab 2: "Related Work Generator"
3. Champ "Option A": sélectionner TOUS les fichiers .md d'un corpus
   ex: corpus_1_rag_basics/*.md (5 fichiers)
4. Entrer un topic dans le champ "Sujet de recherche"
5. Click "Générer"
```

### Step 1b: Via DOIs (Méthode B — dois.txt)

```
1. Go to http://localhost:8000
2. Tab 2: "Related Work Generator"
3. Ouvrir le fichier dois.txt du corpus voulu
4. Coller les DOIs dans "Option B — Liste de DOIs"
5. Entrer un topic
6. Click "Générer"
```

**Formats acceptés:** `.tex`, `.docx`, `.md` (pas `.json`)  
**Corpus disponibles:** chaque dossier contient des fichiers `.md` + `dois.txt`

Expected result: 
- ✅ All papers extracted and indexed
- ✅ Embeddings computed for clustering
- ✅ System ready for generation

### Step 2: Generate with Topic

```
1. Enter a topic from topics.txt
2. Click "Générer"
3. Wait for processing (10-30 seconds typical)
```

Expected result:
- ✅ Section generated
- ✅ All citations from corpus
- ✅ No hallucinations
- ✅ Proper academic format

### Step 3: Verify Results

```
1. Compare generated text to expected_results/generation_guide.md
2. Check:
   - Score/coverage percentage
   - Number of sections
   - Citation accuracy
   - Semantic coherence
3. Look for specific pièges for that corpus
```

## Pièges Explained

### Piège 1: LLM Hallucination

**Problem**: Generated text cites papers NOT in corpus

**Example**:
```
Corpus contains:
- Vaswani et al., "Attention is All You Need" (2017)
- Dosovitskiy et al., "Vision Transformers" (2020)

Generated text (WRONG):
"Initial work by Devlin et al. [BERT] showed strong results..."

ERROR: BERT paper not in corpus!
```

**What system should do**:
- Draft generation might reference BERT
- Self-Refine pass REMOVES it because not in corpus
- Final output only references Vaswani + Dosovitskiy

**How to detect**:
- ❌ FAIL if any paper name mentioned but not in corpus list
- ✅ PASS if all paper names match corpus titles

**Why it matters**:
- Hallucinations undermine scholarly credibility
- Citation verification is core to ScholarCheck
- RAG is supposed to prevent this

---

### Piège 2: Semantic Drift in Clustering

**Problem**: Papers grouped by irrelevant features instead of research theme

**Example**:
```
Corpus: Mix of computer vision, NLP, and RL papers

Good clustering:
- Section 1: Vision papers (ResNet, ViT, YOLO)
- Section 2: NLP papers (BERT, GPT, Transformers)
- Section 3: RL papers (PPO, DQN, A3C)

Bad clustering (semantic drift):
- Section 1: Papers from 2020-2021 (ignores domain)
- Section 2: Papers with >10 authors (ignores domain)
- Section 3: Papers from specific venues (ignores domain)
```

**What system should do**:
- Use embeddings to cluster papers by semantic similarity
- Group papers on same research topic together
- Ignore metadata noise (authors, year, venue)

**How to detect**:
- Read generated sections
- ✅ PASS if each section is coherent and topic-focused
- ❌ FAIL if papers in same section seem unrelated

---

### Piège 3: Empty Abstracts Causing Information Loss

**Problem**: System can't generate proper text when abstracts missing

**corpus_4_minimal** specifically tests this:
```
Paper 1: abstract = null
Paper 2: abstract = ""
Paper 3: abstract = "short phrase only"
```

**What system should do**:
- Use title + year as fallback
- Generate generic but still valid description
- Example: "[Title] (year) contributes to this research area."
- NO crashes or empty output

**How to detect**:
- ❌ FAIL if system crashes on null abstract
- ❌ FAIL if output contains zero text
- ✅ PASS if output still generates coherent section

---

### Piège 4: Conflicting Viewpoints Without False Consensus

**Problem**: System might fabricate agreement where papers disagree

**corpus_3_conflicting** tests this:
```
Paper 1: "Scaling laws predict better performance"
Paper 2: "Transformers have fundamental limitations"
Paper 3: "Scaling has unacceptable environmental cost"
```

**What system should do**:
- Present all three viewpoints
- Do NOT write: "Researchers agree that scaling is beneficial" (FALSE)
- DO write: "Different perspectives exist on scaling trade-offs..."
- Include perspectives from all papers

**How to detect**:
- Read generated text carefully
- ❌ FAIL if contradictory views glossed over
- ❌ FAIL if consensus claimed where none exists
- ✅ PASS if all perspectives fairly represented

---

### Piège 5: Topic Ambiguity and Over-Generalization

**Problem**: Broad topics cause system to include unrelated papers

**Testing ambiguous topics**:
```
Topic: "machine learning"
- Too vague! Matches almost all papers
- System should either:
  * Ask for clarification
  * Pick most relevant N papers
  * Generate broad, multi-theme section

Topic: "retrieval-augmented generation for QA"
- Specific! Should match only RAG + QA papers
- System should generate focused section
```

**How to detect**:
- ✅ PASS if specific topics generate focused sections
- ⚠️ ACCEPTABLE if broad topics generate broad sections
- ❌ FAIL if system includes clearly unrelated papers

---

### Piège 6: Self-Refine Loop Correctness

**Problem**: Refinement pass might accidentally REMOVE correct citations

**Example - WRONG refinement**:
```
Draft generated:
"[Attention is All You Need] introduced transformers. 
[Vision Transformers] applied attention to images."

Corpus contains:
- Vaswani et al., "Attention is All You Need"
- Dosovitskiy et al., "An Image is Worth 16x16 Words"

Refinement prompt sees:
- "[Attention is All You Need]" ✓ in corpus (keep)
- "[Vision Transformers]" ✗ NOT exact match (remove)

Problem: Title doesn't match! Should be "An Image is Worth..."
```

**What system should do**:
- Use fuzzy matching for title verification
- OR instruct LLM to use consistent paper names
- Do NOT remove correct citations due to name variations

**How to detect**:
- ❌ FAIL if correct citations removed during refinement
- ✅ PASS if all valid citations preserved

---

### Piège 7: Coverage vs Hallucination Trade-off

**Problem**: System might either include everything (hallucinate) or include nothing (no coverage)

**Metrics**:
```
Coverage = papers_cited / papers_in_corpus
Hallucination = papers_mentioned_not_in_corpus / papers_mentioned

Ideal: Coverage ~40-60%, Hallucination = 0%

Bad case 1 (over-inclusive):
- Coverage: 95% (tries to cite everything)
- Hallucination: 5% (includes papers not in corpus)

Bad case 2 (under-inclusive):
- Coverage: 5% (cites almost nothing)
- Hallucination: 0% (no hallucinations, but weak output)
```

**How to detect**:
- Count unique papers cited in output
- Divide by corpus size for coverage
- Search output for paper names not in corpus
- ✅ PASS if coverage 40-60% and hallucination ~0%

---

### Piège 8: Generation Without LLM (Fallback Mode)

**Problem**: If LLM fails, template generation might produce low-quality output

**Testing**:
1. Disable all LLM APIs (comment out or use invalid keys)
2. Upload corpus and request generation
3. Verify template mode still produces valid output

**Expected**:
- ✅ System falls back to template mode (100% deterministic)
- ✅ Output is academic-quality even without LLM
- ✅ No hallucinations in template mode

**Template generation should**:
- List papers by cluster
- Use transition phrases
- Include abstracts or descriptive text
- Be organized and readable

---

## Test Combinations

### Test 1: Core RAG (corpus_1_rag_basics)
**Topics**: "retrieval-augmented generation"
**Expected**: 
- All 5 papers cited
- High accuracy
- Clear explanation of RAG concepts

### Test 2: Diverse Corpus (corpus_2_nlp_diversity)  
**Topics**: 
- "pre-training and transfer learning"
- "transformer models and language understanding"
**Expected**: 
- 2-4 thematic sections
- Papers properly clustered
- No off-topic papers included

### Test 3: Conflicting Views (corpus_3_conflicting)
**Topic**: "scaling trade-offs and limitations"
**Expected**:
- All 3 papers represented
- No false consensus
- Balanced presentation of disagreements

### Test 4: Robustness (corpus_4_minimal)
**Topic**: "deep learning optimization"
**Expected**:
- System handles missing abstracts
- No crashes
- Usable output despite sparse metadata

### Test 5: Production Benchmark (corpus_5_comprehensive)
**Topics**: Multiple specific and broad
**Expected**:
- 5-8 thematic sections
- Proper domain clustering
- High coverage without hallucinations
- <30 second generation time

## Success Criteria

### Criterion 1: Zero Hallucinations
```
✅ PASS: Every paper mentioned exists in corpus
❌ FAIL: Any paper cited not in corpus provided
```

### Criterion 2: Adequate Coverage  
```
✅ PASS: 40-60% of corpus papers cited (for focused topic)
✅ PASS: 60-80% of corpus papers cited (for broad topic)
❌ FAIL: <20% cited (insufficient coverage)
❌ FAIL: >90% cited (probably hallucinating or over-inclusive)
```

### Criterion 3: Semantic Coherence
```
✅ PASS: Each section has clear research theme
✅ PASS: Papers within section logically related
❌ FAIL: Random papers mixed in sections
❌ FAIL: Unrelated papers in same section
```

### Criterion 4: Citation Accuracy
```
✅ PASS: All citations reference corpus papers exactly
✅ PASS: Citation format consistent ([Title] or [Author Year])
❌ FAIL: Citations don't match any corpus paper
❌ FAIL: Mixed/inconsistent citation formats
```

### Criterion 5: Robustness
```
✅ PASS: All test cases complete without crashing
✅ PASS: Graceful degradation when abstracts missing
✅ PASS: Handles conflicting viewpoints fairly
❌ FAIL: Crash on edge case
❌ FAIL: Low-quality output when abstracts missing
```

### Criterion 6: Performance  
```
✅ PASS: corpus_1-4 generate in <15 seconds
✅ PASS: corpus_5 generates in <30 seconds
⚠️ WARNING: 30-60 seconds (acceptable but slow)
❌ FAIL: >60 seconds (timeout or inefficiency)
```

## Interpretation Guide

### Score Ranges

**Score = (cited_papers / corpus_papers) × 100%**

```
90-100%: Over-inclusive (probably hallucinating)
70-89%:  Comprehensive (good coverage)
50-69%:  Balanced (appropriate focus)
30-49%:  Selective (concentrated on relevant papers)
<30%:    Under-inclusive (may be missing key content)
```

For specific topics, lower % is acceptable (30-40%).
For broad topics, higher % is expected (60-80%).

### Section Structure

**Good Related Work**:
- 2-4 sections for small corpus (5-10 papers)
- 4-8 sections for large corpus (50+ papers)
- Clear thematic grouping
- Logical flow between sections
- Each paper cited with context

**Bad Related Work**:
- Too many sections (10+) for small corpus
- One giant undifferentiated section
- Papers cited without context
- Redundant explanations across sections

### Quality Indicators

**Hallucination risk**: 0% (exact count)
**Citation accuracy**: 100% (all match corpus)
**Semantic coherence**: Subjective but clear in reading
**Academic tone**: Formal, objective, scholarly
**Completeness**: Covers main themes in corpus

---

## Next Steps After Testing

1. **If all tests pass**: System ready for production use
2. **If some tests fail**:
   - Identify which corpus/topic fails
   - Check specific piège listed in guide
   - Debug based on troubleshooting section
   - Retest after fix
3. **If performance poor**:
   - Profile API calls (embedding, LLM)
   - Check cache effectiveness
   - Optimize corpus parsing
4. **If hallucinations detected**:
   - Review Self-Refine loop
   - Check LLM prompt clarity
   - Test refinement pass in isolation

---

**Testing complete when**:
- ✅ All 5 corpora tested
- ✅ Multiple topics per corpus
- ✅ All zero hallucinations
- ✅ 40-80% coverage (topic-dependent)
- ✅ <30 second generation time
- ✅ Semantic coherence verified
- ✅ Conflicting views handled properly
- ✅ Missing abstracts handled gracefully
