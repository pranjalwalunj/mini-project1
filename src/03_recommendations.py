import os
import pandas as pd
import networkx as nx

EDGES_CSV = "data/processed/edges.csv"
OUT_DIR = "data/processed"
os.makedirs(OUT_DIR, exist_ok=True)

edges = pd.read_csv(EDGES_CSV)
G = nx.from_pandas_edgelist(edges, "src", "dst")

def recommend_friends(user, top_n=15):
    user_neighbors = set(G.neighbors(user))
    candidates = [v for v in G.nodes() if v != user and not G.has_edge(user, v)]

    scores = []
    for v in candidates:
        v_neighbors = set(G.neighbors(v))
        mutual = len(user_neighbors.intersection(v_neighbors))
        if mutual > 0:
            scores.append((user, v, mutual))

    scores.sort(key=lambda x: x[2], reverse=True)
    return pd.DataFrame(scores[:top_n], columns=["user", "recommended", "mutual_friends"])

sample_user = list(G.nodes())[0]
recs = recommend_friends(sample_user, 15)

recs.to_csv(os.path.join(OUT_DIR, "recommendations.csv"), index=False)

print("✅ Recommendations saved to data/processed/recommendations.csv")
print("Sample user:", sample_user)
print(recs.head(10))

