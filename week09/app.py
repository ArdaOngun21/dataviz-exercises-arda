from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="World Happiness 2023", layout="wide")
df = pd.read_csv(Path(__file__).with_name("world_happiness_2023.csv")).rename(columns={
    "Country name": "Country", "Regional indicator": "Region", "Ladder score": "Score"
})
global_mean = df["Score"].mean()
st.title("World happiness in 2023")
st.caption("Source: World Happiness Report 2023 · Course dataset")
region = st.sidebar.selectbox("Region", ["All regions", *sorted(df.Region.unique())])
limit = st.sidebar.slider("Top countries to show", 5, 25, 15)
selected = df if region == "All regions" else df[df.Region == region]
top = selected.nlargest(limit, "Score").sort_values("Score")
a, b, c = st.columns(3)
a.metric("Countries", len(selected))
b.metric("Average happiness", f"{selected.Score.mean():.2f}", f"{selected.Score.mean()-global_mean:+.2f} vs global")
c.metric("Happiest country", top.iloc[-1].Country)
ranking = px.bar(top, x="Score", y="Country", orientation="h", range_x=[0, 10],
                 title=f"Top {len(top)} countries · {region}", labels={"Score": "Happiness score (0–10)", "Country": ""})
st.plotly_chart(ranking, use_container_width=True)

df["Gap"] = df.Score - global_mean
bound = df.Gap.abs().max()
points = df if region == "All regions" else df[df.Region == region]
fig = px.scatter(points, x="Logged GDP per capita", y="Gap", color="Gap",
                 color_continuous_scale="RdBu", range_color=[-bound, bound],
                 hover_name="Country", hover_data={"Region": True, "Score": ":.3f", "Gap": ":+.3f"},
                 labels={"Gap": "Difference from global mean (points)"},
                 title=f"Happiness relative to the global mean · {region}")
fig.update_traces(marker_size=10)
fig.add_hline(y=0, line_dash="dash", annotation_text=f"0 = global mean ({global_mean:.2f}/10)",
              annotation_position="top left")
fig.update_layout(coloraxis_colorbar_title="Gap (points)")
st.plotly_chart(fig, use_container_width=True)
st.caption("Each dot is one country. Blue indicates a score above the unweighted country mean and red indicates a score below it. The benchmark and colour scale stay fixed when you filter regions.")
