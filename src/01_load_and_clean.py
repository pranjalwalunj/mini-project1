import os
import pandas as pd

RAW = "data/raw/facebook_combined.txt"
OUT_DIR = "data/processed"

edges = pd.read_csv(RAW, sep=" ", header=None, names=["src", "dst"]).drop_duplicates()
nodes = pd.DataFrame({"node": pd.unique(edges[["src", "dst"]].values.ravel())})

os.makedirs(OUT_DIR, exist_ok=True)
edges.to_csv(os.path.join(OUT_DIR, "edges.csv"), index=False)
nodes.to_csv(os.path.join(OUT_DIR, "nodes.csv"), index=False)

print("✅ Created:")
print(" - data/processed/edges.csv")
print(" - data/processed/nodes.csv")
print("Edges:", len(edges), "| Nodes:", len(nodes))

