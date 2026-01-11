import pandas as pd
import networkx as nx
import streamlit as st

# ----------------------------
# Page config + small styling
# ----------------------------
st.set_page_config(page_title="Social Network Analytics", layout="wide")

st.markdown(
    """
    <style>
      .block-container {padding-top: 1.2rem; padding-bottom: 2rem;}
      .title-wrap {display:flex; align-items:center; justify-content:space-between;}
      .subtle {opacity:0.85;}
      .card {border:1px solid rgba(49,51,63,0.2); border-radius:14px; padding:14px;}
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------------------
# Load data (cached)
# ----------------------------
@st.cache_data(show_spinner=False)
def load_csvs():
    kpis = pd.read_csv("data/processed/kpis.csv")
    influencers = pd.read_csv("data/processed/top_influencers.csv")
    edges = pd.read_csv("data/processed/edges.csv")
    recs = pd.read_csv("data/processed/recommendations.csv")
    return kpis, influencers, edges, recs

@st.cache_data(show_spinner=False)
def build_graph(edges: pd.DataFrame):
    return nx.from_pandas_edgelist(edges, "src", "dst")

kpis, influencers, edges, recs = load_csvs()
G = build_graph(edges)

# ----------------------------
# Header
# ----------------------------
left, right = st.columns([0.72, 0.28])
with left:
    st.markdown(
        """
        <div class="title-wrap">
          <div>
            <h1 style="margin-bottom:0.2rem;">Social Network Analytics Dashboard</h1>
            <div class="subtle">KPIs • Influencers • Communities • Friend Recommendations</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True
    )
with right:
    st.markdown(
        """
        <div class="card" style="text-align:right; margin-top: 14px;">
          <div class="subtle">Built by</div>
          <div style="font-size:1.1rem; font-weight:700;">Pranjal Walunj</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()

# ----------------------------
# Sidebar controls
# ----------------------------
st.sidebar.header("Controls")

show_rows = st.sidebar.slider("Preview rows", min_value=10, max_value=200, value=25, step=5)

# Let user pick a node for recommendations (if available)
all_nodes = list(G.nodes())
default_user = int(recs["user"].iloc[0]) if not recs.empty else int(all_nodes[0])
selected_user = st.sidebar.selectbox("Select a user for recommendations", all_nodes, index=all_nodes.index(default_user))

top_k = st.sidebar.slider("Top influencers to show", 5, 50, 20, 5)
top_rec_k = st.sidebar.slider("Top recommendations to show", 5, 50, 15, 5)

with st.sidebar.expander("Downloads", expanded=True):
    st.download_button(
        "Download KPIs (kpis.csv)",
        data=kpis.to_csv(index=False).encode("utf-8"),
        file_name="kpis.csv",
        mime="text/csv"
    )
    st.download_button(
        "Download Influencers (top_influencers.csv)",
        data=influencers.to_csv(index=False).encode("utf-8"),
        file_name="top_influencers.csv",
        mime="text/csv"
    )
    st.download_button(
        "Download Recommendations (recommendations.csv)",
        data=recs.to_csv(index=False).encode("utf-8"),
        file_name="recommendations.csv",
        mime="text/csv"
    )

# ----------------------------
# Helper: compute recs on the fly for selected_user (more lively)
# ----------------------------
@st.cache_data(show_spinner=False)
def compute_recs_for_user(edges_df: pd.DataFrame, user: int, top_n: int):
    G_local = nx.from_pandas_edgelist(edges_df, "src", "dst")
    if user not in G_local:
        return pd.DataFrame(columns=["user", "recommended", "mutual_friends"])

    user_neighbors = set(G_local.neighbors(user))
    candidates = [v for v in G_local.nodes() if v != user and not G_local.has_edge(user, v)]

    scores = []
    for v in candidates:
        mutual = len(user_neighbors.intersection(set(G_local.neighbors(v))))
        if mutual > 0:
            scores.append((user, v, mutual))

    scores.sort(key=lambda x: x[2], reverse=True)
    return pd.DataFrame(scores[:top_n], columns=["user", "recommended", "mutual_friends"])

user_recs = compute_recs_for_user(edges, int(selected_user), int(top_rec_k))

# ----------------------------
# KPI row
# ----------------------------
c1, c2, c3, c4, c5, c6 = st.columns(6)

c1.metric("Total Users", int(kpis.loc[0, "total_users"]))
c2.metric("Connections", int(kpis.loc[0, "total_connections"]))
c3.metric("Avg Degree", round(float(kpis.loc[0, "avg_degree"]), 2))
c4.metric("Density", round(float(kpis.loc[0, "density"]), 4))
c5.metric("Communities", int(kpis.loc[0, "num_communities"]))
c6.metric("Components", int(kpis.loc[0, "connected_components"]))

st.markdown(
    f"""
    <div class="card">
      <b>Quick Insight:</b>
      The network is <b>connected</b> (components = {int(kpis.loc[0, "connected_components"])})
      with an average of <b>{round(float(kpis.loc[0, "avg_degree"]), 2)}</b> connections per user.
      Detected <b>{int(kpis.loc[0, "num_communities"])}</b> communities.
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

# ----------------------------
# Tabs
# ----------------------------
tab1, tab2, tab3, tab4 = st.tabs(["📌 Overview", "⭐ Influencers", "🤝 Recommendations", "🧾 Data Preview"])

with tab1:
    left, right = st.columns([0.55, 0.45])

    with left:
        st.subheader("Degree Distribution")
        st.caption("How many connections users have (saved from your analysis).")
        st.image("images/degree_distribution.png", use_container_width=True)

    with right:
        st.subheader("Top Influencers Snapshot")
        st.caption("Top users ranked by PageRank score.")
        top_inf = influencers.head(int(top_k)).copy()

        # Streamlit built-in chart (quick + lively)
        chart_df = top_inf.set_index("node")["pagerank"]
        st.bar_chart(chart_df)

        st.dataframe(top_inf, use_container_width=True)

with tab2:
    st.subheader("Influencers (PageRank)")
    st.caption("Search or filter top influencers.")

    search = st.text_input("Search node id (optional)", value="")
    show_inf = influencers.head(int(top_k)).copy()

    if search.strip():
        # show exact match if possible
        try:
            node_id = int(search.strip())
            match = influencers[influencers["node"] == node_id]
            if not match.empty:
                st.success("Found matching node in influencer list.")
                st.dataframe(match, use_container_width=True)
            else:
                st.warning("Node not in top influencer list. Showing current top list.")
        except:
            st.warning("Please enter a valid integer node id.")

    st.dataframe(show_inf, use_container_width=True)

with tab3:
    st.subheader("Friend Recommendations (Mutual Friends)")
    st.caption("Pick a user from the sidebar to generate recommendations live.")

    a, b = st.columns([0.55, 0.45])
    with a:
        st.markdown(
            f"""
            <div class="card">
              <b>Selected user:</b> {selected_user}<br/>
              <span class="subtle">Recommendations are ranked by number of mutual friends.</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.dataframe(user_recs, use_container_width=True)

    with b:
        # Simple contextual stats for selected user
        try:
            deg = G.degree(int(selected_user))
            st.markdown(
                f"""
                <div class="card">
                  <b>User Stats</b><br/>
                  Connections (degree): <b>{deg}</b><br/>
                  Showing top <b>{top_rec_k}</b> recommendations
                </div>
                """,
                unsafe_allow_html=True
            )
        except:
            st.info("User stats unavailable for selected node.")

with tab4:
    st.subheader("Raw & Processed Data")
    st.caption("Quick previews to validate pipelines (use slider in sidebar).")

    st.markdown("**Edges (sample)**")
    st.dataframe(edges.head(int(show_rows)), use_container_width=True)

    st.markdown("**Recommendations (sample)**")
    st.dataframe(recs.head(int(show_rows)), use_container_width=True)

    st.markdown("**KPIs**")
    st.dataframe(kpis, use_container_width=True)

