from flask import request, jsonify
from app import app
from util import load_data, moran_local_regression, plot_moran_local

@app.route('/moran_local', methods=['POST'])
def moran_local_api():
    data = request.get_json()
    csv_file_path = data['csv_file_path']

    gdf = load_data(csv_file_path)
    moran_loc = moran_local_regression(gdf)
    plot_moran_local(moran_loc, gdf)

    return jsonify({'message': 'Moran Local Regression plot generated.'})
