import numpy as np
import plotly.graph_objects as go
import streamlit as st


def calculate_beers(pubs, hangover, kiwi, participants, kebab):
    kebab_factor = 1 + kebab / 1000  # Increase beers by 1% per gram of kebab
    kiwi_factor = 1.5 if kiwi else 1.0
    base_beers = ((10 - hangover) / 5) * (participants / 10)

    # Enhanced non-linear scaling using exponential function
    max_pubs = 10
    non_linear_factor = (np.exp(pubs / max_pubs) - 1) / (np.e - 1)

    beers = base_beers * non_linear_factor * 15 * kebab_factor

    return max(0, min(beers, pubs * 2)) * kiwi_factor  # Limit max beers to 2 per pub


st.set_page_config(layout="wide")

st.title(
    "🍺 Petur's totally scientific Pre-Marathon Pub Crawl Beer Calculator 🏃 (2024 version)"
)

# Move all options to the sidebar
st.sidebar.header("Pub Crawl Parameters")
kiwi = st.sidebar.checkbox("Kiwi constant (Are you a 🥝?)")
hangover = st.sidebar.slider(
    "Hangover susceptibility index (higher more susceptible)", 1, 10, 5
)
participants = st.sidebar.slider(
    "Number of crawl participants (peer pressure) ", 5, 25, 10
)
kebab = st.sidebar.slider(
    "Volume of kebab consumed post-drinking (grams)", 0, 1000, 200
)

# Fixed number of planned pubs
planned_pubs = 6

# Calculate beers for the current settings
current_beers = calculate_beers(planned_pubs, hangover, kiwi, participants, kebab)
st.write(f"Recommended beers for your {planned_pubs}-pub crawl: {current_beers:.2f}")

# Create a plot showing beers vs number of pubs using Plotly
pub_range = list(range(1, 11))  # Keep max number of pubs at 10
beers_range = [
    calculate_beers(p, hangover, kiwi, participants, kebab) for p in pub_range
]

fig = go.Figure()

# Add line and markers for all pubs
fig.add_trace(
    go.Scatter(
        x=pub_range,
        y=beers_range,
        mode="lines+markers",
        name="Beer Trajectory",
        line=dict(color="blue", width=2),
        marker=dict(size=10, symbol="diamond", color="gold"),
    )
)

# Add a special marker for the planned number of pubs
fig.add_trace(
    go.Scatter(
        x=[planned_pubs],
        y=[current_beers],
        mode="markers",
        name="Planned number of pubs",
        marker=dict(size=20, symbol="star", color="red"),
    )
)

fig.update_layout(
    title="Recommended Beers vs Number of Pubs",
    xaxis_title="Number of Pubs",
    yaxis_title="Recommended Beers",
    hovermode="x unified",
)

# Set x-axis to show only integer values
fig.update_xaxes(tick0=1, dtick=1, range=[0.5, 10.5])

# Set y-axis to start from 0
fig.update_yaxes(range=[0, 21])

# Add custom hover text
fig.update_traces(hovertemplate="Pubs: %{x}<br>Beers: %{y:.2f}<extra></extra>")

st.plotly_chart(fig, use_container_width=True)
st.sidebar.write("Generated mainly using Claude.ai (3.5 Sonnet)")
