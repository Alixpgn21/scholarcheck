# Test 6: Edge Cases and Boundary Conditions

This document tests boundary conditions and edge cases that stress the system's robustness.

## Ultra-Old References

References from the early history of science should be handled gracefully.

**Reference:** Newton, I. (1687). "Philosophiæ Naturalis Principia Mathematica." Royal Society of London.

**Reference:** Euler, L. (1748). "Introductio in analysin infinitorum." Academia Imperialis Scientiarum Petropolitanae.

**Reference:** Descartes, R. (1637). "La Géométrie." Appendix to Discourse on Method.

Expected behavior: `not_found` (papers predate modern indexing) or minimal information.

## Future Dates (Impossible)

**Reference:** Future, A., Researcher, B. (2050). "Artificial superintelligence fully solved." Journal of Future Science, 2050.

**Reference:** Tomorrow, T. (2099). "Quantum gravity unified theory." Physics Quarterly, 2099.

Expected behavior: `not_found` (papers haven't been published yet).

## Single Author References

**Reference:** Goodfellow, I. (2014). "Generative adversarial networks." arXiv preprint arXiv:1406.2661. DOI: 10.48550/arXiv.1406.2661

Note: While technically co-authored, should still be resolvable.

## Many Authors (>10)

**Reference:** Hinton, G. E., Srivastava, N., Krizhevsky, A., Sutskever, I., Salakhutdinov, R. R., Droplet, J., et al. (2012). "Improving neural networks by preventing co-adaptation of feature detectors." arXiv preprint arXiv:1207.0580. DOI: 10.48550/arXiv.1207.0580

Expected behavior: APIs should handle "et al." notation or return the primary authors.

## Accented Author Names

**Reference:** Müller, Z., & François, P. (2019). "Machine learning for physics." European Journal of AI, 12(3):234-256. DOI: 10.1234/ej.2019.012

**Reference:** Pérez-García, J., & López-Hernández, M. (2018). "Deep neural networks in biomedics." Medical Computing Review, 5(2):123-145. DOI: 10.1234/mcr.2018.005

Expected behavior: Author names with diacritics should be properly matched.

## Hyphenated Surnames

**Reference:** Pouget-Abadie, J., Warde-Farley, D., Mirza, M., Xu, B., Goodfellow, I., Bengio, Y., & Courville, A. (2014). "Generative adversarial networks." arXiv preprint arXiv:1406.2661. DOI: 10.48550/arXiv.1406.2661

Expected behavior: Hyphenated names like "Pouget-Abadie" and "Warde-Farley" should not be split.

## CamelCase Author Names

**Reference:** LeCun, Y., Bottou, L., & Bengio, Y. (1998). "Gradient-based learning applied to document recognition." Proceedings of the IEEE, 86(11):2278-2324. DOI: 10.1109/5.726791

**Reference:** DeCoste, D., & Schoelkopf, B. (2002). "Training invariant support vector machines." Machine Learning, 46(1-3):161-190. DOI: 10.1023/A:1012454411458

Expected behavior: Names like "LeCun" and "DeCoste" should be recognized as single units.

## arXiv DOIs (Often Not Indexed)

**Reference:** Dosovitskiy, A., Beyer, L., Kolesnikov, A., et al. (2020). "An image is worth 16x16 words: Transformers for image recognition at scale." arXiv preprint arXiv:2010.11929. DOI: 10.48550/arXiv.2010.11929

Expected behavior: May return `not_found` due to API indexing limitations (not a hallucination, but an API limitation).

## References Without DOI (Title-Only Search)

**Reference:** Bengio, Y., Goodfellow, I., & Courville, A. (2013). "Representation learning: A review and perspectives." IEEE Transactions on Pattern Analysis and Machine Intelligence, 35(8):1798-1828.

Expected behavior: Should still resolve via title/author matching even without DOI.

## Very Short Titles

**Reference:** Smith, J. (2015). "AI." Journal of Computing, 2015.

**Reference:** Lee, K. (2020). "ML." Technical Report.

Expected behavior: May struggle to disambiguate (too generic), likely `not_found` or low confidence.

## Very Long Titles (>150 characters)

**Reference:** Vaswani, A., et al. (2017). "Attention is All You Need: A Novel Architecture Based Solely on Attention Mechanisms, Eliminating the Need for Recurrence and Convolutions in Sequence-to-Sequence Models." NeurIPS.

Expected behavior: Truncation or normalization should still allow matching.

## Publisher-Specific Variations

**Reference (Nature):** Author, A. (2020). "Title of paper." Nature, 580(7803):123-128.

**Reference (IEEE):** Author, B. (2020). "Title of paper." IEEE Transactions on Systems, Man, and Cybernetics: Systems, 50(5):1234-1245.

**Reference (JMLR):** Author, C. (2020). "Title of paper." Journal of Machine Learning Research, 21(45):1-20.

**Reference (ACM):** Author, D. (2020). "Title of paper." ACM Transactions on Graphics, 39(6):1-15.

Expected behavior: All should resolve if papers exist in respective venues.

## Special Characters in Titles

**Reference:** Martinez-Garcia, J. (2018). "Back-propagation & gradient descent: Theory & practice." Computational Science & Engineering, 2018.

**Reference:** O'Neill, B. (2020). "The O'Reilly guide to machine learning's future." O'Reilly Media.

Expected behavior: Ampersands, apostrophes, hyphens should not break parsing.

## Year Variants

**Reference:** Late-submitted 2022 paper published in 2023: Smith, J. (2023). "Title." Journal. (Original submission year: 2022)

**Reference:** Multiple versions: arXiv 2019, published 2020, revised 2021.

Expected behavior: System should match on most recent or published year.

## DOI Format Variants

**Standard DOI:** 10.1109/CVPR.2015.7298965

**DOI.org URL:** https://doi.org/10.1109/CVPR.2015.7298965

**dx.doi.org URL:** https://dx.doi.org/10.1109/CVPR.2015.7298965

**arXiv DOI:** 10.48550/arXiv.1706.03762

Expected behavior: All formats should resolve or normalize properly.

## Mixed Language References

**Reference (German):** Müller, H. (2015). "Die Maschinen Lernen: Ein Überblick." Informatik Journal, 2015.

**Reference (French):** Lefevre, P. (2018). "L'apprentissage profond et ses applications." Revue d'Informatique, 2018.

**Reference (Mixed):** Schwarz, K., & García, J. (2019). "Deep Learning for Image Recognition: Ein umfassender Überblick." International Journal of Computer Science, 2019.

Expected behavior: Gracefully handle non-English metadata.

---

## Expected Results Summary

| Edge Case | Expected Status | Confidence | Reason |
|-----------|-----------------|-----------|--------|
| 1687 publication | `not_found` | 0.0 | Pre-digital |
| 2050 future date | `not_found` | 0.0 | Not published |
| Single author | `ok` or `warning` | 0.5-1.0 | Resolvable |
| 10+ authors | `ok` | 0.5-1.0 | APIs handle "et al." |
| Accented names | `ok` | 0.5-1.0 | Unicode support |
| Hyphenated names | `ok` | 0.5-1.0 | Depends on API |
| CamelCase names | `ok` | 0.5-1.0 | Regex-dependent |
| arXiv DOI | `not_found` or `warning` | 0.0-0.5 | API limitation |
| No DOI | `ok` or `not_found` | 0.3-1.0 | Title fallback |
| Very short title | `not_found` | 0.0 | Too generic |
| Very long title | `ok` or `warning` | 0.3-1.0 | Truncation handling |
| Special characters | `ok` | 0.5-1.0 | Parser dependent |
| Old years | `not_found` | 0.0 | Pre-digital |
| DOI URL variants | `ok` | 0.8-1.0 | Normalization |
| Non-English | `ok` or `warning` | 0.3-0.8 | Limited support |

---

## Why Edge Cases Matter

These tests verify that ScholarCheck:
1. **Doesn't crash** on unusual input
2. **Gracefully degrades** when APIs can't resolve
3. **Distinguishes** between API limitations and actual hallucinations
4. **Handles character sets** properly (Unicode, special chars)
5. **Normalizes input** correctly (URL formats, author names)
