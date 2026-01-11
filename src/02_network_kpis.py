import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Paths
EDGES_CSV = "data/processed/edges.csv"
OUT_DIR = "data/processed"
IMG_DIR = "images"

os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)

# Load edges and build graph
edges = pd.read_csv(EDGES_CSV)
G = nx.from_pandas_edgelist(edges, "src", "dst")

# --- KPIs ---
kpis = {
    "total_users": G.number_of_nodes(),
    "total_connections": G.number_of_edges(),
    "density": nx.density(G),
    "avg_degree": sum(dict(G.degree()).values()) / G.number_of_nodes(),
    "connected_components": nx.number_connected_components(G),
}

# Community detection (graduate-level)
from networkx.algorithms.community import greedy_modularity_communities
communities = list(greedy_modularity_communities(G))
kpis["num_communities"] = len(communities)

# Influencers (PageRank)
pagerank = nx.pagerank(G)
top_influencers = (
    pd.DataFrame(sorted(pagerank.items(), key=lambda x: x[1], reverse=True), columns=["node", "pagerank"])
    .head(20)
)

# Save KPIs
kpis_df = pd.DataFrame([kpis])
kpis_df.to_csv(os.path.join(OUT_DIR, "kpis.csv"), index=False)

# Save influencers
top_influencers.to_csv(os.path.join(OUT_DIR, "top_influencers.csv"), index=False)

# --- Plot: Degree distribution ---
degrees = [d for _, d in G.degree()]
plt.figure()
plt.hist(degrees, bins=50)
plt.title("Degree Distribution")
plt.xlabel("Degree")
plt.ylabel("User Count")
plt.savefig(os.path.join(IMG_DIR, "degree_distribution.png"), dpi=200, bbox_inches="tight")

print("✅ KPIs saved to data/processed/kpis.csv")
print("✅ Influencers saved to data/processed/top_influencers.csv")
print("✅ Plot saved to images/degree_distribution.png")
print("KPIs:", kpis)
print("\nTop 5 influencers:\n", top_influencers.head(5))

