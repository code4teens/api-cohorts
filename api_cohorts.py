from flask import Blueprint, jsonify, request

from database import db_session
from models import Cohort
from schemata import CohortSchema

api_cohorts = Blueprint('api_cohorts', __name__)


@api_cohorts.route('/cohorts')
def get_cohorts():
    cohorts = Cohort.query.order_by(Cohort.id).all()
    data = CohortSchema(many=True).dump(cohorts)

    return jsonify(data), 200


@api_cohorts.route('/cohorts', methods=['POST'])
def create_cohort():
    keys = ['name', 'nickname', 'duration', 'start_date']

    if sorted([key for key in request.json]) == sorted(keys):
        cohort_schema = CohortSchema()

        try:
            cohort = cohort_schema.load(request.json)
        except Exception as _:
            data = {
                'title': 'Bad Request',
                'status': 400,
                'detail': 'Some values failed validation'
            }

            return data, 400
        else:
            db_session.add(cohort)
            db_session.commit()
            data = {
                'title': 'Created',
                'status': 201,
                'detail': f'Cohort {cohort.id} created'
            }

            return data, 201
    else:
        data = {
            'title': 'Bad Request',
            'status': 400,
            'detail': 'Missing some keys or contains extra keys'
        }

        return data, 400
