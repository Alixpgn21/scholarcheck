"""
Clustering thématique des documents par embeddings.
"""
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


def cluster_documents(embeddings: np.ndarray, documents: list[dict], max_clusters: int = 8) -> list[dict]:
    """
    Détermine automatiquement le nombre optimal de clusters (2..max_clusters)
    en maximisant le silhouette score, puis assigne chaque document à un cluster.
    """
    n = len(documents)
    if n < 3:
        for doc in documents:
            doc["cluster"] = 0
        return [{"cluster_id": 0, "documents": documents, "label": "Unique cluster"}]

    best_k, best_score = 2, -1
    k_range = range(2, min(max_clusters + 1, n))

    for k in k_range:
        km = KMeans(n_clusters=k, random_state=42, n_init="auto")
        labels = km.fit_predict(embeddings)
        score = silhouette_score(embeddings, labels)
        if score > best_score:
            best_k, best_score = k, score

    km = KMeans(n_clusters=best_k, random_state=42, n_init="auto")
    labels = km.fit_predict(embeddings)

    clusters: dict[int, list] = {i: [] for i in range(best_k)}
    for doc, label in zip(documents, labels):
        doc["cluster"] = int(label)
        clusters[int(label)].append(doc)

    return [
        {"cluster_id": cid, "documents": docs, "label": f"Thème {cid + 1}"}
        for cid, docs in clusters.items()
    ]


def get_cluster_representatives(cluster: dict, embeddings: np.ndarray, all_documents: list[dict], top_k: int = 3) -> list[dict]:
    """Retourne les top_k documents les plus centraux d'un cluster."""
    cluster_docs = cluster["documents"]
    cluster_indices = [all_documents.index(d) for d in cluster_docs]
    cluster_embs = embeddings[cluster_indices]

    centroid = cluster_embs.mean(axis=0)
    distances = np.linalg.norm(cluster_embs - centroid, axis=1)
    sorted_indices = np.argsort(distances)

    return [cluster_docs[i] for i in sorted_indices[:top_k]]
