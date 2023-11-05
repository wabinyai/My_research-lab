from flask import Flask, render_template
from util import load_data, moran_local_regression, plot_moran_local
from configure import Config
import os

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def index():
    df = load_data(os.getenv('CSV_FILE_PATH'))
    moran_loc = moran_local_regression(df)
    plot_moran_local(moran_loc, df)
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
