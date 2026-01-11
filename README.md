# Social Network Analytics Dashboard

## 📌 Project Overview
This project analyzes a large-scale social network to uncover key insights such as influential users, community structures, and potential friend recommendations. Using real-world Facebook network data, the project applies graph analytics and interactive visualization to simulate how platforms like Facebook or LinkedIn analyze user connections.

The final output is an **interactive Streamlit dashboard** designed for data analysts and product teams.

---

## 🎯 Business Problem
Social platforms need to:
- Identify **influential users**
- Understand **community structures**
- Recommend new connections
- Monitor network growth and engagement

This project demonstrates how **network analytics** can solve these problems using real data.

---

## 📂 Dataset
- **Source:** Stanford SNAP – Ego Facebook Dataset  
- **Nodes:** 4,039 users  
- **Edges:** 88,234 connections  
- **Type:** Undirected social graph  

🔗 https://snap.stanford.edu/data/egonets-Facebook.html

---

## ⚙️ Tech Stack
- Python
- Pandas
- NetworkX
- Matplotlib
- Streamlit
- Git & GitHub

---

## 📊 Key Analytics & KPIs
- Total Users
- Total Connections
- Network Density
- Average Degree
- Connected Components
- Community Detection
- Influencer Ranking (PageRank)

---

## ⭐ Influencer Detection
- PageRank algorithm used to identify high-impact users
- Top influencers ranked based on network centrality

---

## 🤝 Friend Recommendation System
- Recommends new connections based on **mutual friends**
- Simulates real social network recommendation logic

---

## 📈 Visualizations
- Degree Distribution
- Influencer Bar Charts
- KPI Metrics
- Interactive Tables

---

## 🖥 Dashboard
The Streamlit dashboard allows:
- Live KPI exploration
- Influencer filtering
- User-based friend recommendations
- CSV downloads for analysis

---

## ▶️ How to Run Locally
```bash
git clone <your-repo-url>
cd mini-project1
pip install -r requirements.txt
streamlit run dashboard/app.py
