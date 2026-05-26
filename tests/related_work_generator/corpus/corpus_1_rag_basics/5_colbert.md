# ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT

**Authors:** Omar Khattab, Matei Zaharia
**Year:** 2020
**Venue:** SIGIR
**DOI:** 10.1145/3397271.3401075
**URL:** https://arxiv.org/abs/2004.12832

## Abstract

Ranking architectures for retrieval-based question answering have traditionally made early interaction between the query and document representations. Dense retrieval has shown strong performance, but at considerable computational cost. In this work, we propose ColBERT, which uses deep contextual language models to represent queries and passages with learned late-interaction ColBERT scoring. We show that ColBERT significantly outperforms prior retrieval methods, including dense passage retrieval and strong sparse baselines, on multiple QA benchmarks. Importantly, ColBERT achieves competitive accuracy while being much faster than existing dense retrieval methods through an efficient retrieval algorithm. Our approach makes it practical to apply contextual language models to large-scale retrieval problems.
