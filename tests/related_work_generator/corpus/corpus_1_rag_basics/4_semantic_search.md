# Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks

**Authors:** Nils Reimers, Iryna Gurevych
**Year:** 2019
**Venue:** EMNLP
**DOI:** 10.18653/v1/D19-1410
**URL:** https://arxiv.org/abs/1908.10084

## Abstract

BERT and other transformer models have achieved state-of-the-art results in many NLP tasks. However, finding the most similar sentence pair in a collection of 10,000 sentences requires about 50 million inference computations with BERT, which is not practical. We propose Sentence-BERT (SBERT), which modifies the pretrained BERT network architecture to produce semantically meaningful sentence embeddings. Sentence embeddings can be compared using cosine similarity, which is computationally efficient. We evaluate our approach on various tasks including semantic search, semantic textual similarity, clustering, and duplicate detection. The results demonstrate that the proposed SBERT is computationally efficient while achieving competitive performance compared to BERT-based approaches. Our models are made publicly available.
