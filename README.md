# Social Network Analytics Dashboard

An end-to-end social network analytics project using real Facebook network data to compute KPIs, identify influencers, detect communities, and generate friend recommendations. Includes an interactive Streamlit dashboard for exploration.

## Dataset
- Source: Stanford SNAP (Ego-Facebook)
- Nodes: 4,039
- Edges: 88,234

## Tech Stack
- Python, Pandas
- NetworkX
- Matplotlib
- Streamlit

## Key Features
- Network KPIs: users, connections, density, avg degree, connected components, communities
- Influencer detection using PageRank
- Friend recommendations using mutual friends
- Streamlit dashboard with filters, charts, and CSV downloads

## How to Run
```bash
pip install -r requirements.txt
streamlit run dashboard/app.py

