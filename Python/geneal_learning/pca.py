import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import plotly.express as px

# Sample HCP data
df = pd.DataFrame({
    'HCP_ID': [f'HCP_{i+1}' for i in range(10)],
    'Rx_count': [120, 80, 200, 50, 300, 180, 90, 60, 250, 130],
    'churn_score': [0.2, 0.8, 0.1, 0.5, 0.3, 0.4, 0.7, 0.6, 0.2, 0.3],
    'social_media_score': [70, 20, 90, 10, 50, 60, 30, 15, 85, 40],
    'num_publications': [5, 0, 12, 1, 8, 6, 2, 0, 10, 4],
    'research_interest': ['cardiology', 'oncology', 'neurology', 'oncology', 'cardiology', 'neurology', 'oncology', 'cardiology', 'neurology', 'oncology'],
    'specialty': ['internal medicine', 'oncology', 'neurology', 'oncology', 'cardiology', 'neurology', 'oncology', 'cardiology', 'neurology', 'oncology'],
    'sub_specialty': ['diabetes', 'breast cancer', 'stroke', 'lung cancer', 'hypertension', 'epilepsy', 'melanoma', 'heart failure', 'parkinson', 'leukemia']
})

# Encode categorical features
df_encoded = pd.get_dummies(df.drop('HCP_ID', axis=1), drop_first=True)

# Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_encoded)

# KMeans clustering
kmeans = KMeans(n_clusters=3, random_state=42)
df['Cluster'] = kmeans.fit_predict(X_scaled)

# PCA for visualization
pca = PCA(n_components=2)
components = pca.fit_transform(X_scaled)
df['PC1'] = components[:, 0]
df['PC2'] = components[:, 1]

# Plot PCA clusters
fig = px.scatter(
    df,
    x='PC1',
    y='PC2',
    color='Cluster',
    hover_data=['HCP_ID', 'Rx_count', 'churn_score', 'num_publications'],
    title='PCA Visualization of HCP Clusters',
    template='plotly_white'
)
fig.show()

# Rank HCPs based on weighted score (example formula)
df['HCP_rank_score'] = (
    df['Rx_count'] * 0.4 +
    df['social_media_score'] * 0.2 +
    df['num_publications'] * 0.3 -
    df['churn_score'] * 100 * 0.1
)

df['HCP_rank'] = df['HCP_rank_score'].rank(ascending=False).astype(int)

# Display ranked HCPs
ranked_df = df[['HCP_ID', 'Cluster', 'HCP_rank_score', 'HCP_rank']].sort_values(by='HCP_rank')
print(ranked_df)


==============================

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

# Simulated data
np.random.seed(42)
n_samples = 200
n_features = 6
n_clusters = 3

X = np.random.rand(n_samples, n_features)
labels = np.random.choice(n_clusters, n_samples)

df = pd.DataFrame(X, columns=[f'Feature_{i+1}' for i in range(n_features)])
df['Cluster'] = labels

st.title("🧠 Unsupervised Segmentation Explainability")

# PCA Scatter Plot
st.subheader("📉 PCA Scatter Plot")
pca = PCA(n_components=2)
components = pca.fit_transform(df.drop('Cluster', axis=1))
scatter_df = pd.DataFrame(components, columns=['PC1', 'PC2'])
scatter_df['Cluster'] = df['Cluster'].astype(str)

fig = px.scatter(scatter_df, x='PC1', y='PC2', color='Cluster', title='PCA Cluster Visualization')
st.plotly_chart(fig)

# Cluster-wise Feature Heatmap
st.subheader("🔥 Cluster-wise Feature Heatmap")
cluster_means = df.groupby('Cluster').mean()
fig, ax = plt.subplots()
sns.heatmap(cluster_means, annot=True, cmap='viridis', ax=ax)
st.pyplot(fig)

# Radar Chart
st.subheader("🕸️ Radar Chart of Cluster Profiles")
selected_cluster = st.selectbox("Select cluster", cluster_means.index)
values = cluster_means.loc[selected_cluster].values
categories = cluster_means.columns.tolist()

radar_fig = go.Figure()
radar_fig.add_trace(go.Scatterpolar(
    r=values,
    theta=categories,
    fill='toself',
    name=f'Cluster {selected_cluster}'
))
radar_fig.update_layout(polar=dict(radialaxis=dict(visible=True)), showlegend=True)
st.plotly_chart(radar_fig)