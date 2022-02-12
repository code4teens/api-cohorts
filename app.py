from flask import Flask

from api_cohorts import api_cohorts
from database import db_session

app = Flask(__name__)
app.register_blueprint(api_cohorts)


@app.teardown_appcontext
def close_session(exception=None):
    db_session.remove()
