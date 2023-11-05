import pandas as pd
import geopandas as gpd
from pysal.explore import esda
import libpysal
import matplotlib.pyplot as plt

def load_data(csv_file_path):
    data = pd.read_csv(csv_file_path)
    gdf = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data.site_longitude, data.site_latitude))
    return gdf

def moran_local_regression(gdf):
    w = libpysal.weights.DistanceBand.from_dataframe(gdf, threshold=100, binary=True)
    moran_loc = esda.Moran_Local(gdf['pm2_5_calibrated_value'], w)
    return moran_loc

def plot_moran_local(moran_loc, gdf):
    # Create a new category column based on cluster types
    gdf['cluster_category'] = ['HH' if c == 1 else 'LH' if c == 2 else 'LL' if c == 3 else 'HL' if c == 4 else 'NS' for c in moran_loc.q]
    f, ax = plt.subplots(1, figsize=(10, 10))
    gdf.plot(column='cluster_category', categorical=True, k=5, cmap='brg', linewidth=0.1, ax=ax, edgecolor='grey', legend=True)
    plt.title("Local Moran's I Cluster Map for PM2.5")
    plt.show()
