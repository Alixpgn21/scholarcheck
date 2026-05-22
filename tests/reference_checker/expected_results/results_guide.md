# Reference Checker Expected Results Guide

This document provides the expected results and interpretation for each test document.

---

## Test 1: Basic Correct References

**File:** `test_1_basic_correct.tex`  
**Type:** Gold standard - all references should verify correctly

### Expected Outcome

```
✅ Status: PASSED
Score: 95-100%
Total references: 7
Results breakdown:
  - ok: 7 (100%)
  - warning: 0
  - not_found: 0
  - suspect: 0
Average confidence: 0.85-1.0
```

### Per-Reference Expected Results

| Reference | Expected Status | Confidence | Notes |
|-----------|-----------------|-----------|-------|
| Vaswani 2017 (Attention) | ok | 0.95-1.0 | Verified by all 3 APIs, highly cited |
| He 2015 (ResNet) | ok | 0.95-1.0 | Verified by all 3 APIs, landmark paper |
| Cortes 1995 (SVM) | ok | 0.9-1.0 | Classical paper, well-indexed |
| Polack 2020 (Vaccine) | ok | 0.95-1.0 | Recent, high-impact, clear semantics |
| Bergstra 2012 (Hyperparams) | ok | 0.85-0.95 | JMLR indexed, consistent metadata |
| Hamilton 2017 (GNN) | ok | 0.9-0.95 | NeurIPS paper, well-documented |

### What to Look For

✅ All references should return "ok" status  
✅ Confidence should be consistently high (>0.8)  
✅ Zero warnings or semantic issues  
✅ Abstracts should be retrieved successfully  
✅ All metadata (year, authors) should match exactly  

### Troubleshooting

| Issue | Likely Cause | Action |
|-------|------------|--------|
| One paper shows `warning` | API metadata inconsistency | Acceptable - cross-check manually |
| Confidence < 0.8 | API indexing lag | Acceptable for older papers |
| One shows `not_found` | Indexing issue | Check API status, retry |

**Acceptable range:** 85-100% score (some API inconsistencies expected)

---

## Test 2: Complete Hallucinations

**File:** `test_2_hallucinations.tex`  
**Type:** Negative test - all fabricated references

### Expected Outcome

```
✅ Status: PASSED
Score: 0-5%
Total references: 7
Results breakdown:
  - ok: 0
  - warning: 0
  - not_found: 7 (100%)
  - suspect: 0
Confidence: 0.0 (all papers)
Message (all): "No sources found this reference"
```

### Per-Reference Expected Results

| Reference | Expected Status | Confidence | Why Not Found |
|-----------|-----------------|-----------|---------------|
| Smith 2024 (Quantum Teleportation) | not_found | 0.0 | Fake journal + fake DOI |
| Johnson 2023 (Machine Consciousness) | not_found | 0.0 | No such paper exists |
| Newton 1850 (Victorian AI) | not_found | 0.0 | Anachronistic + date mismatch |
| Thompson 2024 (Perpetual Motion) | not_found | 0.0 | Violates physics |
| Goldman 2023 (Age Reversal) | not_found | 0.0 | Miraculous claim, unverified |
| Williams 2024 (FTL Communication) | not_found | 0.0 | Impossible physics |
| Brown 2023 (Cold Fusion) | not_found | 0.0 | Historical hoax |

### What to Look For

✅ **All** references should return `not_found`  
✅ **No** reference should have any match  
✅ Confidence should be **exactly 0.0** for all  
✅ No API should return a match  
✅ System should not hallucinate alternative papers  

### Troubleshooting

| Issue | Likely Cause | Action |
|-------|------------|--------|
| One or two show `ok` | Accidental match in API | Very unlikely - verify DOI |
| Confidence > 0 on any | Partial match detected | Investigate which API returned it |
| System hangs | API timeout | Check API connectivity |

**Pass criteria:** ALL 7 must be `not_found` with 0.0 confidence

---

## Test 3: Metadata Errors

**File:** `test_3_metadata_errors.md`  
**Type:** Papers exist but metadata has errors

### Expected Outcome

```
✅ Status: PASSED
Score: 40-60%
Total references: 6
Results breakdown:
  - ok: 2-3
  - warning: 3-4
  - not_found: 0-1
  - suspect: 0
Average confidence: 0.27-0.5
```

### Per-Reference Expected Results

| Reference | Expected Status | Confidence | Issue | Reason |
|-----------|-----------------|-----------|-------|--------|
| ResNet 2012 (not 2015) | warning | 0.3-0.5 | Year mismatch | Paper found (correct year 2015), but citation says 2012 |
| Attention 2010 (not 2014) | warning | 0.3-0.5 | Year mismatch | Paper found (correct year 2014), but citation says 2010 |
| Recommenders wrong authors | warning | 0.35-0.45 | Author mismatch | DOI resolves, but authors don't match |
| GANs incomplete authors | warning | 0.4-0.5 | Partial match | Found but author list incomplete |
| BERT 2019 incomplete | warning | 0.35-0.45 | Year + author errors | Multiple mismatches compound penalty |
| U-Net 2010 (not 2015) | warning | 0.3-0.5 | Year mismatch | Paper found with correct year 2015 |

### What to Look For

✅ Most should return `warning` status  
✅ Confidence should be reduced (0.3-0.5 range)  
✅ Messages should indicate specific mismatches:
  - "Year mismatch: expected 2015, found 2012"
  - "Authors not found: [list]"
✅ Papers should still be found (not `not_found`)  
✅ Penalty should reflect severity (1-2 year difference = mild penalty)

### Troubleshooting

| Issue | Likely Cause | Action |
|-------|------------|--------|
| Some show `ok` instead of `warning` | Metadata extraction failed | Check NLI/author regex |
| All show `not_found` | DOI resolution broken | Check API endpoints |
| Confidence too high (>0.7) | Penalty calculation off | Review confidence formula |
| Some missing error messages | Message generation bug | Check message templates |

**Pass criteria:** Majority should be `warning` with 0.3-0.5 confidence

---

## Test 4: Semantic Traps

**File:** `test_4_semantic_traps.txt`  
**Type:** References exist but semantic contradiction detected

### Expected Outcome

```
✅ Status: PASSED
Score: 50-70% (papers found, but semantic issues)
Total references: 6
Results breakdown:
  - ok: 6
  - warning: 0
  - not_found: 0
  - suspect: 6 (NLI badge)
NLI scores: 0.7-0.95 (high contradiction)
```

### Per-Reference Expected Results

| Reference | Reference Status | NLI Status | NLI Score | Reason |
|-----------|------------------|-----------|-----------|--------|
| Vaccine ineffective (vs efficacy) | ok | suspect | 0.8-0.95 | Direct contradiction |
| Climate natural causes (vs anthropogenic) | ok | suspect | 0.85-0.95 | Direct contradiction |
| GPT-4 = AGI (vs capability limits) | ok | ambigu | 0.7-0.85 | Overstatement/ambiguous |
| Deep learning brain enhancement | ok | suspect | 0.75-0.9 | Unsupported causal claim |
| Attention = explainable (vs "not explanation") | ok | suspect | 0.8-0.9 | Explicit contradiction |
| Medical cure (vs prevention) | ok | suspect | 0.8-0.9 | Different medical claims |

### What to Look For

✅ **All** papers should be found (`ok` status)  
✅ **All** should have NLI badge: `suspect` or `ambigu`  
✅ NLI scores should be HIGH (0.7-0.95)  
✅ Messages should explain the contradiction:
  - "Abstract contradicts the citing statement"
  - "Claim not supported by paper"
✅ Confidence should distinguish:
  - Reference confidence: 0.8-1.0 (paper is valid)
  - NLI score: 0.7-0.95 (semantic problem)

### Troubleshooting

| Issue | Likely Cause | Action |
|-------|------------|--------|
| NLI badge missing | NLI module not running | Check if abstracts retrieved |
| NLI score too low (<0.5) | NLI model not triggered | Verify cross-encoder working |
| All show `not_found` | API lookup failed | Check API connectivity |
| Some show "ok" without badge | NLI threshold too high | Review scoring thresholds |

**Pass criteria:** All papers found, all have NLI badge with high scores (>0.7)

---

## Test 5: Mixed Cases

**File:** `test_5_mixed_cases.tex`  
**Type:** Realistic mix of ok/warning/not_found

### Expected Outcome

```
✅ Status: PASSED
Score: 50-60%
Total references: 11
Results breakdown:
  - ok: 5 (45%)
  - warning: 3 (27%)
  - not_found: 2 (18%)
  - suspect: 1 (9%)
Average confidence: 0.50-0.65
```

### Per-Reference Expected Results

| # | Reference | Status | Confidence | Notes |
|---|-----------|--------|-----------|-------|
| 1 | Vaswani 2017 | ok | 0.95-1.0 | Classic paper |
| 2 | Bahdanau 2015 | ok | 0.9-0.95 | ICLR paper |
| 3 | He 2016 (not 2015) | warning | 0.4-0.5 | Year mismatch |
| 4 | Devlin 2018 | ok | 0.95-1.0 | BERT, well-known |
| 5 | Radford 2018 | ok | 0.85-0.95 | GPT paper |
| 6 | Smith 2024 Quantum | not_found | 0.0 | Fabricated |
| 7 | Johnson 2023 DNA | not_found | 0.0 | Fabricated |
| 8 | Hamilton 2017 | ok | 0.9-0.95 | GNN paper |
| 9 | Dosovitskiy 2020 | ok | 0.9-1.0 | ViT paper |
| 10 | Polack 2020 Wrong | ok+suspect | 0.85-0.95 + 0.85 | Semantic trap |
| 11 | Neural 2023 Brain | not_found | 0.0 | Fabricated |

### What to Look For

✅ Realistic distribution of results  
✅ ~45% ok, ~27% warning, ~18% not_found, ~9% suspect  
✅ Hallucinations clearly identified (score 0.0)  
✅ Metadata errors flagged as warnings (0.3-0.5)  
✅ Semantic contradictions detected with NLI  
✅ Valid papers confirmed (>0.8 confidence)

### Troubleshooting

| Issue | Likely Cause | Action |
|-------|------------|--------|
| Score too high (>70%) | False positives on hallucinations | Check API matching |
| Score too low (<40%) | False negatives on real papers | Check API connectivity |
| Missing NLI badge | Abstract not retrieved | Verify fallback chain |
| Unbalanced distribution | Random API failures | Retry test |

**Pass criteria:** 50-60% score with realistic distribution

---

## Test 6: Edge Cases

**File:** `test_6_edge_cases.md`  
**Type:** Boundary conditions and robustness testing

### Expected Outcome

```
✅ Status: PASSED
Behavior: No crashes, graceful degradation
Score: 30-50%
Key points:
  - System handles unusual input without crashing
  - Clear distinction between API limitations and hallucinations
  - Character encoding works correctly
```

### Critical Edge Cases

| Edge Case | Expected Status | Confidence | Behavior |
|-----------|-----------------|-----------|----------|
| 1687 publication | not_found | 0.0 | Pre-digital, not indexed |
| 2050 future paper | not_found | 0.0 | Not published yet |
| Single author | ok | 0.8-1.0 | Should work |
| 10+ authors with "et al." | ok | 0.8-1.0 | APIs handle well |
| Accented names (Müller, Pérez) | ok | 0.7-0.95 | Unicode support |
| Hyphenated names (Pouget-Abadie) | ok | 0.8-1.0 | Regex improvement |
| CamelCase names (LeCun, DeCoste) | ok | 0.8-1.0 | Pattern matching |
| arXiv DOI | not_found or warning | 0.0-0.5 | API limitation (not hallucination) |
| No DOI (title only) | ok or not_found | 0.3-1.0 | Fallback search |
| Very short title "AI" | not_found | 0.0 | Too generic |
| Very long title (150+ chars) | ok or warning | 0.3-0.95 | Truncation handling |
| Special characters (&, -, ', etc.) | ok | 0.8-1.0 | Parser handles |

### What to Look For

✅ **Zero crashes** - system should handle all input gracefully  
✅ **Clear messaging** - distinguish:
   - "Paper not found (hallucination)" vs
   - "Paper not indexed by APIs (limitation)"  
✅ **Character support** - diacritics, hyphens, special chars  
✅ **Metadata extraction** - handles compound surnames  
✅ **Confidence penalties** - reflect actual uncertainty, not arbitrary  

### Troubleshooting

| Issue | Likely Cause | Action |
|-------|------------|--------|
| Crash on accented chars | Encoding bug | Check UTF-8 support |
| Hyphenated names split | Regex issue | Use enhanced pattern |
| CamelCase names broken | Case-sensitive parsing | Make case-insensitive |
| All arXiv marked hallucination | No distinction logic | Add "API limitation" message |
| System hangs on edge case | Infinite loop | Add timeout, debug query |

**Pass criteria:** 
- No crashes
- Graceful degradation on all edge cases
- Clear messaging about limitations vs hallucinations

---

## Test 7: Comprehensive Test (Production Benchmark)

**File:** `test_7_comprehensive.tex`  
**Type:** Full system test with 29+ references, all types mixed

### Expected Outcome

```
✅ Status: PASSED
Score: 44-50%
Total references: 32
Results breakdown:
  - ok: 13 (40%)
  - warning: 5 (16%)
  - not_found: 11 (34%)
  - suspect: 3 (9%)
Processing time: <30 seconds
Memory: <500MB
Average confidence: 0.45-0.55
```

### Distribution Analysis

| Category | Count | % | Expected Status |
|----------|-------|---|-----------------|
| Correct papers | 13 | 40% | ok (0.8-1.0 conf) |
| Metadata errors | 5 | 16% | warning (0.3-0.5 conf) |
| Hallucinations | 11 | 34% | not_found (0.0 conf) |
| Semantic traps | 3 | 9% | ok + suspect |

### Performance Expectations

| Metric | Expected | Threshold |
|--------|----------|-----------|
| Total time | <30s | <60s max |
| API calls | ~96 (3 APIs × 32) | Parallelized OK |
| Caching hits | 10-15% | Expected on repeats |
| Memory peak | <500MB | <1GB max |
| Error rate | <2% | <5% acceptable |

### What to Look For

✅ Distribution should match realistic paper mix  
✅ Processing completes in <30 seconds  
✅ Score in 44-50% range (realistic hallucination + error rate)  
✅ No memory leaks (memory stable)  
✅ Clear per-reference reporting  
✅ Summary statistics accurate  

### Per-Reference Groups

**Group 1: Correct (13)**
- All should be `ok` with high confidence (>0.8)
- Typical papers: Vaswani, He, Devlin, etc.

**Group 2: Metadata Errors (5)**
- All should be `warning` with reduced confidence (0.3-0.5)
- Identified issues: Year mismatch, author mismatch

**Group 3: Hallucinations (11)**
- All should be `not_found` with 0.0 confidence
- Includes fabricated journals, impossible claims

**Group 4: Semantic Traps (3)**
- Papers found (`ok`) but NLI flags `suspect`
- Examples: vaccine contradiction, climate denial

### Troubleshooting

| Issue | Likely Cause | Action |
|-------|------------|--------|
| Score >60% | False positives on hallucinations | Verify DOI matching logic |
| Score <40% | False negatives on real papers | Check API connectivity |
| Time >60s | API timeout or inefficient parallelization | Profile API calls |
| Memory spike | Caching not clearing | Check cache cleanup |
| Incomplete results | Partial API failure | Check error handling |
| Wrong distribution | Test data issue | Verify reference mix |

### Success Criteria

- ✅ Score between 44-50% (±5% acceptable)
- ✅ All correct papers found with high confidence
- ✅ All hallucinations flagged as not_found
- ✅ Metadata errors identified as warnings
- ✅ Semantic contradictions flagged with NLI
- ✅ Processing completes in <30 seconds
- ✅ No memory leaks or crashes
- ✅ Clear, actionable reporting for each reference

**This is the production-readiness benchmark.**

---

## Summary: Expected Scores by Test

| Test | File | Expected Score | Key Metric |
|------|------|-----------------|-----------|
| 1 | test_1_basic_correct.tex | 95-100% | All ok, high confidence |
| 2 | test_2_hallucinations.tex | 0-5% | All not_found, 0.0 conf |
| 3 | test_3_metadata_errors.md | 40-60% | Warnings with 0.3-0.5 conf |
| 4 | test_4_semantic_traps.txt | 50-70% | Ok papers + NLI suspect |
| 5 | test_5_mixed_cases.tex | 50-60% | Realistic distribution |
| 6 | test_6_edge_cases.md | 30-50% | No crashes, graceful |
| 7 | test_7_comprehensive.tex | 44-50% | Full benchmark test |

---

## Interpretation Quick Reference

### Status Meanings

```
✅ ok (Green)
   → Reference found, metadata matches, no semantic issues
   → Confidence: 0.5-1.0 (higher = more reliable)
   → Action: Safe to use - no concerns

⚠️ warning (Yellow)
   → Reference found BUT something doesn't match
   → Possible issues:
     * Year off by >1 year
     * Authors don't match expected
     * Confidence reduced due to inconsistency
   → Confidence: 0.27-0.47
   → Action: Manual verification recommended

❌ not_found (Red)
   → No API found this reference
   → Possible causes:
     * Hallucination (paper doesn't exist)
     * API limitation (not yet indexed)
     * Very new paper or preprint
   → Confidence: 0.0
   → Action: Manual search or cite with caution

🚨 suspect (Dark Orange) - NLI Badge
   → Paper exists but semantic contradiction detected
   → Status: Still "ok" for the paper itself
   → Issue: How it's being cited/interpreted
   → Score: 0.7-0.9 (high contradiction)
   → Action: Review how paper is being cited
```

### Confidence Score Ranges

```
0.9-1.0  = Highly reliable (found by all APIs, perfect match)
0.7-0.9  = Reliable (found by 2+ APIs, minor discrepancies)
0.5-0.7  = Moderate (found by 1 API or some metadata mismatch)
0.3-0.5  = Problematic (found but significant issues)
0.0-0.3  = Unreliable (not found or major contradictions)
0.0      = Not found (hallucination or API gap)
```

### Hallucination Risk Assessment

```
Hallucination Risk = (not_found + suspect_NLI) / total_refs

Risk Levels:
  >10%  = High (article needs audit before publication)
  5-10% = Medium (check flagged references carefully)
  <5%   = Low (references appear sound)

Formula: If 32 refs, expect:
  >3.2 problematic = high risk
  1.6-3.2 problematic = medium risk
  <1.6 problematic = low risk
```

---

## How to Use This Guide

1. **Before testing**: Read expected results for that test
2. **During testing**: Compare actual output to table
3. **If mismatch**: Check troubleshooting section
4. **After testing**: Document deviations and root causes
5. **Iterate**: Fix issues, retest, verify results within expected range

Each test is independent and focuses on a specific problem domain. Together, they provide comprehensive coverage of ScholarCheck's reference verification capabilities.
