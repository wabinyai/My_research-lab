import pandas as pd
import geopandas as gpd
from libpysal.weights import Queen
from libpysal.explore.esda.moran import Moran_Local
import matplotlib.pyplot as plt

def load_data(csv_file_path):
    data = pd.read_csv(csv_file_path)
    gdf = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data.site_longitude, data.site_latitude))
    return gdf

def moran_local_regression(gdf):
    w = Queen.from_dataframe(gdf)
    moran_loc = Moran_Local(gdf.pm2_5_calibrated_value, w)
    return moran_loc

def plot_moran_local(moran_loc, gdf):
    fig, ax = moran_loc.plot_local_autocorrelation(plot=False, p=0.05)
    gdf.assign(cl=1).plot(column='cl', categorical=True, legend=True, ax=ax)
    plt.show()
