import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="IPL Cricket Statistics Dashboard",
    page_icon="🏏",
    layout="wide"
)

# ---------------- LOAD DATA ----------------

df = pd.read_csv("player.csv")

# ---------------- SIDEBAR ----------------

st.sidebar.title("🏏 IPL Dashboard Filters")

teams = ["All"] + sorted(df["TEAM"].unique().tolist())
selected_team = st.sidebar.selectbox("Select Team", teams)

if selected_team != "All":
    filtered_df = df[df["TEAM"] == selected_team]
else:
    filtered_df = df.copy()

st.sidebar.markdown("---")
st.sidebar.info(
    """
    **IPL Cricket Statistics Dashboard**

    Developed using:
    - Python
    - Streamlit
    - Pandas
    - Plotly
    """
)

# ---------------- TITLE ----------------

st.title("🏏 IPL Cricket Statistics Dashboard")
st.caption("Built using Python • Streamlit • Pandas • Plotly")
st.write(
    "This dashboard provides interactive analysis of IPL teams, players, runs, wickets and match statistics."
)

# ---------------- KPI CARDS ----------------

total_runs = filtered_df["RUNS"].sum()
total_wickets = filtered_df["WICKETS"].sum()
total_players = filtered_df["PLAYER"].nunique()
total_matches = filtered_df["MATCH"].nunique()

c1, c2, c3, c4 = st.columns(4)

c1.metric("🏏 Total Runs", total_runs)
c2.metric("🏆 Total Wickets", total_wickets)
c3.metric("👤 Players", total_players)
c4.metric("🎯 Matches", total_matches)

st.divider()
st.subheader("🏆 Tournament Leaders")

c1, c2 = st.columns(2)

top_batsman = filtered_df.groupby("PLAYER")["RUNS"].sum()
top_bowler = filtered_df.groupby("PLAYER")["WICKETS"].sum()

with c1:
    st.success(
        f"🏏 Orange Cap Winner\n\n"
        f"👤 {top_batsman.idxmax()}\n\n"
        f"🏏 Runs : {top_batsman.max()}"
    )

with c2:
    st.success(
        f"🏆 Purple Cap Winner\n\n"
        f"👤 {top_bowler.idxmax()}\n\n"
        f"🎯 Wickets : {top_bowler.max()}"
    )

st.divider()

# ---------------- ORANGE & PURPLE CAP ----------------

orange = (
    filtered_df.groupby("PLAYER")["RUNS"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

purple = (
    filtered_df.groupby("PLAYER")["WICKETS"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

left, right = st.columns(2)

with left:
    fig1 = px.bar(
        x=orange.index,
        y=orange.values,
        title="🟠 Orange Cap - Top Run Scorers",
        color=orange.values,
        color_continuous_scale="Oranges",
        text=orange.values,
        labels={"x": "Player", "y": "Runs"}
    )

    fig1.update_traces(textposition="outside")
    fig1.update_layout(
    xaxis_tickangle=-45,
    height=500
)
    st.plotly_chart(fig1, use_container_width=True)

with right:
    fig2 = px.bar(
        x=purple.index,
        y=purple.values,
        title="🟣 Purple Cap - Top Wicket Takers",
        color=purple.values,
        color_continuous_scale="Purples",
        text=purple.values,
        labels={"x": "Player", "y": "Wickets"}
    )

    fig2.update_traces(textposition="outside")
    fig2.update_layout(
    xaxis_tickangle=-45,
    height=500
)
    st.plotly_chart(fig2, use_container_width=True)

# ---------------- TEAM COMPARISON ----------------

st.divider()

st.subheader("🏏 Team Performance")

col1, col2 = st.columns(2)

team_runs = (
    filtered_df.groupby("TEAM")["RUNS"]
    .sum()
    .sort_values(ascending=False)
)

team_wickets = (
    filtered_df.groupby("TEAM")["WICKETS"]
    .sum()
    .sort_values(ascending=False)
)

with col1:
    fig3 = px.bar(
        x=team_runs.index,
        y=team_runs.values,
        title="🏏 Team-wise Total Runs",
        color=team_runs.values,
        color_continuous_scale="Viridis",
        text=team_runs.values,
        labels={"x": "Team", "y": "Runs"}
    )

    fig3.update_traces(textposition="outside")
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    fig4 = px.bar(
        x=team_wickets.index,
        y=team_wickets.values,
        title="🏆 Team-wise Total Wickets",
        color=team_wickets.values,
        color_continuous_scale="Blues",
        text=team_wickets.values,
        labels={"x": "Team", "y": "Wickets"}
    )

    fig4.update_traces(textposition="outside")
    st.plotly_chart(fig4, use_container_width=True)
    

# ---------------- MATCH STATISTICS ----------------

st.divider()

st.subheader("📈 Match-wise Runs")

match_runs = (
    filtered_df.groupby("MATCH")["RUNS"]
    .sum()
    .reset_index()
)

fig5 = px.line(
    match_runs,
    x="MATCH",
    y="RUNS",
    markers=True,
    title="Runs Scored in Each Match"
)

st.plotly_chart(fig5, use_container_width=True)
st.divider()

st.subheader("🥧 Team-wise Runs Distribution")

team_runs = filtered_df.groupby("TEAM")["RUNS"].sum().reset_index()

fig7 = px.pie(
    team_runs,
    names="TEAM",
    values="RUNS",
    hole=0.4,
    title="Runs Contribution by Team"
)

st.plotly_chart(fig7, use_container_width=True)
st.subheader("📊 Player Performance Analysis")

player_stats = filtered_df.groupby("PLAYER")[["RUNS","WICKETS"]].sum().reset_index()

fig8 = px.scatter(
    player_stats,
    x="RUNS",
    y="WICKETS",
    size="RUNS",
    color="WICKETS",
    hover_name="PLAYER",
    title="Runs vs Wickets Analysis"
)

fig8.update_traces(
    marker=dict(line=dict(width=1, color="black"))
)
st.plotly_chart(fig8,use_container_width=True)
# ---------------- PLAYER PERFORMANCE ----------------

st.divider()

st.subheader("👤 Player Performance")

players = sorted(filtered_df["PLAYER"].unique())

selected_player = st.selectbox(
    "Select Player",
    players
)

player_data = filtered_df[
    filtered_df["PLAYER"] == selected_player
]

fig6 = px.bar(
    player_data,
    x="MATCH",
    y="RUNS",
    color="RUNS",
    text="RUNS",
    title=f"{selected_player} Runs in Each Match"
)

fig6.update_traces(textposition="outside")

fig6.update_layout(
    xaxis_tickangle=-45,
    height=500
)

st.plotly_chart(fig6, use_container_width=True)

# ---------------- DATASET ----------------

st.divider()

st.subheader("📋 Complete Dataset")

st.dataframe(filtered_df, use_container_width=True)

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Dataset",
    data=csv,
    file_name="ipl_data.csv",
    mime="text/csv"
)
st.markdown("---")
st.markdown(
    "<center><h5>🏏 IPL Cricket Statistical Dashboard | Developed by Rohan Yadav</h5></center>",
    unsafe_allow_html=True
)