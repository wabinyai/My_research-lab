# app.wsgi

import sys
sys.path.insert(0, '/src/report')

activate_this = '/src/report/venv/bin/activate'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

from app import get_air_quality_data as application