"""
Clustering thématique des documents par embeddings.
"""
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

def _inject_graph_features(embeddings: np.ndarray, documents: list[dict], alpha: float = 0.8) -> np.ndarray:
    """
    Graph RAG: Combine les embeddings sémantiques purs avec les liens de citations (Graphe).
    alpha contrôle le poids du texte pur vs le graphe (1.0 = texte seul, 0.0 = graphe seul).
    """
    n = len(documents)
    if n < 2:
        return embeddings
        
    # Création de la matrice d'adjacence
    adj = np.zeros((n, n))
    id_to_idx = {doc.get("openalex_id"): i for i, doc in enumerate(documents) if doc.get("openalex_id")}
    
    for i, doc in enumerate(documents):
        refs = doc.get("referenced_works", [])
        for ref in refs:
            if ref in id_to_idx:
                j = id_to_idx[ref]
                adj[i, j] = 1.0
                adj[j, i] = 1.0  # Rendre non orienté pour rapprocher les deux
                
    # Normalisation de la matrice (moyenne des voisins)
    row_sums = adj.sum(axis=1)
    # Éviter la division par zéro
    row_sums[row_sums == 0] = 1.0
    adj_normalized = adj / row_sums[:, np.newaxis]
    
    # Message Passing (Graph Convolution simple)
    # Le nouvel embedding est un mix entre le sien et la moyenne de ses voisins
    neighbor_embeddings = adj_normalized @ embeddings
    
    # On applique l'injection uniquement pour les noeuds ayant des voisins
    has_neighbors = (adj.sum(axis=1) > 0).reshape(-1, 1)
    new_embeddings = np.where(
        has_neighbors,
        alpha * embeddings + (1 - alpha) * neighbor_embeddings,
        embeddings
    )
    
    # Re-normaliser
    norms = np.linalg.norm(new_embeddings, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return new_embeddings / norms


def cluster_documents(embeddings: np.ndarray, documents: list[dict], max_clusters: int = 8) -> list[dict]:
    """
    Détermine automatiquement le nombre optimal de clusters (2..max_clusters)
    en maximisant le silhouette score sur les embeddings enrichis par le Graph RAG.
    """
    n = len(documents)
    if n < 3:
        for doc in documents:
            doc["cluster"] = 0
        return [{"cluster_id": 0, "documents": documents, "label": "Unique cluster"}]

    # Phase 5: Graph RAG Injection
    enriched_embeddings = _inject_graph_features(embeddings, documents, alpha=0.8)

    best_k, best_score = 2, -1
    k_range = range(2, min(max_clusters + 1, n))

    for k in k_range:
        km = KMeans(n_clusters=k, random_state=42, n_init="auto")
        labels = km.fit_predict(enriched_embeddings)
        score = silhouette_score(enriched_embeddings, labels)
        if score > best_score:
            best_k, best_score = k, score

    km = KMeans(n_clusters=best_k, random_state=42, n_init="auto")
    labels = km.fit_predict(enriched_embeddings)

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
