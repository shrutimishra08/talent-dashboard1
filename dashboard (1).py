import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title("RedBull AI Talent Matching Dashboard")

# Precomputed personas (replace with your Colab output)
personas = {
    'Sales': {'Diplomatic': 85.80, 'Balanced': 87.10, 'Sociable': 78.30, 'Innovative': 83.00, 'SalesRevenue': 485000.00, 'MarketShare': 5.09},
    'Retail': {'Diplomatic': 78.60, 'Balanced': 81.00, 'Sociable': 87.30, 'Innovative': 71.00, 'SalesRevenue': 406700.00, 'MarketShare': 4.06},
    'Product': {'Diplomatic': 70.50, 'Balanced': 86.50, 'Sociable': 76.70, 'Innovative': 90.60, 'EBIT': 502000.00, 'ProjectDeliveryRate': 90.00},
    'HR': {'Diplomatic': 86.50, 'Balanced': 90.50, 'Sociable': 80.60, 'Innovative': 76.30, 'RetentionRate': 85.50},
    'Legal': {'Diplomatic': 90.40, 'Balanced': 85.60, 'Sociable': 70.40, 'Innovative': 80.60, 'ComplianceRate': 95.10}
}

# Display personas
st.header("Department Personas")
persona_df = pd.DataFrame(personas).T
st.dataframe(persona_df.round(2))

# Candidate input
st.header("Candidate WingFinder Input")
diplomatic = st.slider("Diplomatic", 0, 100, 85)
balanced = st.slider("Balanced", 0, 100, 90)
sociable = st.slider("Sociable", 0, 100, 75)
innovative = st.slider("Innovative", 0, 100, 80)

# Match candidate
def match_candidate(diplomatic, balanced, sociable, innovative):
    candidate = np.array([diplomatic, balanced, sociable, innovative])
    distances = {}
    for dept in personas:
        persona_scores = np.array([personas[dept][m] for m in ['Diplomatic', 'Balanced', 'Sociable', 'Innovative']])
        distance = np.sqrt(np.sum((candidate - persona_scores) ** 2))
        distances[dept] = distance
    best_match = min(distances, key=distances.get)
    return best_match, distances

if st.button("Match Candidate"):
    best_dept, distances = match_candidate(diplomatic, balanced, sociable, innovative)
    st.success(f"Recommended Department: {best_dept}")
    st.subheader("Match Scores (Lower is Better)")
    dist_df = pd.DataFrame(list(distances.items()), columns=['Department', 'Distance'])
    st.dataframe(dist_df.round(2))
    fig = px.bar(dist_df, x='Department', y='Distance', title='Candidate Match Scores')
    st.plotly_chart(fig)