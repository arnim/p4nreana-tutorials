import pandas as pd
import numpy as np
import umap
import matplotlib.pyplot as plt



def get_random_data(nrow=1000,rnd=42):
    np.random.seed(rnd)
    num_rows = nrow
    num_columns = 4
    data = np.random.rand(num_rows, num_columns)
    column_names = [f"C_{i+1}" for i in range(num_columns)]
    df = pd.DataFrame(data, columns=column_names)
    return df

def project_umap(df):
    # UMAP projection
    umap_model = umap.UMAP(n_components=2, random_state=42)
    umap_projection = umap_model.fit_transform(df)
    return umap_projection[:, 0], umap_projection[:, 1]

df=get_random_data()
x,y=project_umap(df)

df["x_umap"]=x
df["y_umap"]=y

first_column_values = df["C_1"].values.reshape(-1, 1)
scaler = MinMaxScaler()
umap_projection_scaled = scaler.fit_transform(first_column_values)

# Color points based on the scaled values of the first component
plt.scatter(df["x_umap"], df["y_umap"], c=umap_projection_scaled[:, 0], cmap='jet')

# Add colorbar for reference
cbar = plt.colorbar()
cbar.set_label('Scaled UMAP Dimension 1')

plt.title('UMAP Projection of DataFrame with Scaled Color')
plt.xlabel('UMAP Dimension 1')
plt.ylabel('UMAP Dimension 2')
plt.savefig('plot.png')