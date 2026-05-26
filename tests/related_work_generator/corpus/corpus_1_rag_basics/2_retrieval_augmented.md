# Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks

**Authors:** Patrick Lewis, Ethan Perez, Aleksandara Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih, Tim Rocktäschel, Sebastian Riedel, Douwe Kiela
**Year:** 2020
**Venue:** NeurIPS
**DOI:** 10.48550/arXiv.2005.11401
**URL:** https://arxiv.org/abs/2005.11401

## Abstract

Large language models have shown impressive performance on a range of downstream NLP tasks. However, their ability to access and manipulate knowledge is still limited compared to task-specific architectures. Additionally, parametric knowledge stored in model weights can easily become stale. In this work, we explore how to augment language models with the ability to access and manipulate knowledge from external sources as they generate text, without modifying model architecture. We introduce the Retrieval-Augmented Generation (RAG) framework, which combines a pre-trained retriever (DPR) with a pre-trained seq2seq model (BART). We compare RAG to a strong baseline of retrieving and ranking based on TF-IDF + BM25 in addition to the latest dense retrieval methods. We show that retrieval-augmentation using dense retriever outperforms the BM25 baseline significantly. Furthermore, the RAG framework can be integrated with various retrieval indices and different model architectures. Results demonstrate that augmenting language models with retrieval improves generation quality.
