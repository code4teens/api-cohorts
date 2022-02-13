from flask import Blueprint, jsonify, request
from sqlalchemy import exc

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


@api_cohorts.route('/cohorts/<int:id>')
def get_cohort(id):
    cohort = Cohort.query.filter_by(id=id).one_or_none()

    if cohort is not None:
        data = CohortSchema().dump(cohort)

        return data, 200
    else:
        data = {
            'title': 'Not Found',
            'status': 404,
            'detail': f'Cohort {id} not found'
        }

        return data, 404


@api_cohorts.route('/cohorts/<int:id>', methods=['PUT'])
def update_cohort(id):
    keys = [
        'name',
        'nickname',
        'duration',
        'start_date',
        'review_schema',
        'feedback_schema'
    ]

    if all(key in keys for key in request.json):
        existing_cohort = Cohort.query.filter_by(id=id).one_or_none()

        if existing_cohort is not None:
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
                cohort.id = existing_cohort.id
                db_session.merge(cohort)

                try:
                    db_session.commit()
                except exc.IntegrityError as _:
                    data = {
                        'title': 'Bad Request',
                        'status': 400,
                        'detail': 'Some values failed validation'
                    }

                    return data, 400
                else:
                    data = cohort_schema.dump(existing_cohort)

                    return data, 200
        else:
            data = {
                'title': 'Not Found',
                'status': 404,
                'detail': f'Cohort {id} not found'
            }

            return data, 404
    else:
        data = {
            'title': 'Bad Request',
            'status': 400,
            'detail': 'Missing some keys or contains extra keys'
        }

        return data, 400


@api_cohorts.route('/cohorts/<int:id>', methods=['DELETE'])
def delete_cohort(id):
    cohort = Cohort.query.filter_by(id=id).one_or_none()

    if cohort is not None:
        db_session.delete(cohort)
        db_session.commit()
        data = {
            'title': 'OK',
            'status': 200,
            'detail': f'Cohort {id} deleted'
        }

        return data, 200
    else:
        data = {
            'title': 'Not Found',
            'status': 404,
            'detail': f'Cohort {id} not found'
        }

        return data, 404
