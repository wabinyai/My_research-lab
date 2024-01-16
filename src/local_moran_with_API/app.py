from flask import Flask, render_template, request
from utils import fetch_data_from_api, get_data_for_moran, moran_local_regression, plot_folium_map
from datetime import datetime , timedelta

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        grid_id = request.form.get('grid_id')
        start_time = datetime.strptime(request.form.get('start_time'), '%Y-%m-%dT%H:%M')
        end_time = datetime.strptime(request.form.get('end_time'), '%Y-%m-%dT%H:%M')
    else:
        # Specify the airqloud_id
        grid_id = "64b7baccf2b99f00296acd59"
        start_time = datetime.now() - timedelta(days=14)
        end_time = datetime.now()

    page = 1

    # Call the function with the desired start and end times
    data = fetch_data_from_api(grid_id, start_time, end_time, page)

    if data:
        # Get the GeoDataFrame with relevant data
        gdf = get_data_for_moran(data)
        # Check if 'calibratedValue' is present before dropping NaN values
        if 'calibratedValue' in gdf.columns:
            print("Number of NaN values in calibratedValue:", gdf['calibratedValue'].isna().sum())
            gdf = gdf.dropna(subset=['calibratedValue'])
            print(gdf.info())
            # Calculate Local Moran's I
            moran_loc = moran_local_regression(gdf)
            plot_folium_map(moran_loc, gdf)
            print("Local Moran's I saved in cluster_map.html")
            # plot_moran_local(moran_loc, gdf)

            # Render the template with the Folium map and pass the gdf variable
            return render_template('index.html', gdf=gdf)

        else:
            print("No measurements for this search.")
            return "No measurements for this search."

    else:
        print("Failed to fetch data from the API.")
        return "Failed to fetch data from the API."

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error_message="Page not found"), 404

# Custom error handler for general exceptions
@app.errorhandler(Exception)
def handle_exception(e):
    return render_template('error.html', error_message=str(e)), 500

if __name__ == '__main__':
    app.run(debug=True)
 