# Dense Passage Retrieval for Open-Domain Question Answering

**Authors:** Vladimir Karpukhin, Barlas Oğuz, Sewon Min, Patrick Lewis, Ledell Wu, Sergey Edunov, Mike Lewis, Wen-tau Yih
**Year:** 2020
**Venue:** EMNLP
**DOI:** 10.18653/v1/2020.emnlp-main.550
**URL:** https://arxiv.org/abs/1909.10506

## Abstract

Open-domain question answering relies on efficient passage retrieval to select candidate contexts, where traditional sparse vector space models, such as TF-IDF or BM25, are the de facto method. In this work, we show that retrieval can be practically implemented with dense representations alone, in which embeddings are learned from weak supervision of question-passage pairs that can be obtained without relevance annotations. When applied to a large set of Wikipedia passages, our dense retriever substantially outperforms a strong Lucene-BM25 baseline on two open-domain QA benchmarks. Moreover, for many porter questions, our dense retriever is able to retrieve relevant passages even when they do not share any lexical overlap with the question. We also compare against the sparse-dense hybrid approach of an array of dense methods. Our results suggest that retrieval with dense representations is viable and can substantially improve both the speed and accuracy of open-domain question answering systems.
