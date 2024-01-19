import pandas as pd
import numpy as np
import umap
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

# Set the seed for reproducibility
np.random.seed(42)

# Create a DataFrame with random numbers
num_rows = 100
num_columns = 10
data = np.random.rand(num_rows, num_columns)
column_names = [f"Column_{i+1}" for i in range(num_columns)]
df = pd.DataFrame(data, columns=column_names)

# UMAP projection
umap_model = umap.UMAP(n_components=2, random_state=42)
umap_projection = umap_model.fit_transform(df)

# PCA projection
pca_model = PCA(n_components=2, random_state=42)
pca_projection = pca_model.fit_transform(df)

# t-SNE projection
tsne_model = TSNE(n_components=2, random_state=42)
tsne_projection = tsne_model.fit_transform(df)

# Add UMAP, t-SNE, and PCA coordinates as columns in the DataFrame
df['x_umap'] = umap_projection[:, 0]
df['y_umap'] = umap_projection[:, 1]
df['x_pca'] = pca_projection[:, 0]
df['y_pca'] = pca_projection[:, 1]
df['x_tsne'] = tsne_projection[:, 0]
df['y_tsne'] = tsne_projection[:, 1]

# Scale the values for better colors
scaler = MinMaxScaler()
umap_scaled = scaler.fit_transform(umap_projection[:, 0].reshape(-1, 1))
pca_scaled = scaler.fit_transform(pca_projection[:, 0].reshape(-1, 1))
tsne_scaled = scaler.fit_transform(tsne_projection[:, 0].reshape(-1, 1))

# Create subplots
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# UMAP plot
axes[0].scatter(umap_projection[:, 0], umap_projection[:, 1], c=umap_scaled[:, 0], cmap='viridis')
axes[0].set_title('UMAP Projection')
axes[0].set_xlabel('UMAP Dimension 1')
axes[0].set_ylabel('UMAP Dimension 2')
cbar0 = fig.colorbar(axes[0].collections[0], ax=axes[0])
cbar0.set_label('Scaled UMAP Dimension 1')

# PCA plot
axes[1].scatter(pca_projection[:, 0], pca_projection[:, 1], c=pca_scaled[:, 0], cmap='viridis')
axes[1].set_title('PCA Projection')
axes[1].set_xlabel('PCA Dimension 1')
axes[1].set_ylabel('PCA Dimension 2')
cbar1 = fig.colorbar(axes[1].collections[0], ax=axes[1])
cbar1.set_label('Scaled PCA Dimension 1')

# t-SNE plot
axes[2].scatter(tsne_projection[:, 0], tsne_projection[:, 1], c=tsne_scaled[:, 0], cmap='viridis')
axes[2].set_title('t-SNE Projection')
axes[2].set_xlabel('t-SNE Dimension 1')
axes[2].set_ylabel('t-SNE Dimension 2')
cbar2 = fig.colorbar(axes[2].collections[0], ax=axes[2])
cbar2.set_label('Scaled t-SNE Dimension 1')

# Adjust layout and save the figure
plt.tight_layout()
plt.savefig('projections_comparison.png')

# Show the plot
plt.show()

# Display the DataFrame with added columns
print(df.head())
