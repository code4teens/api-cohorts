from marshmallow import fields, post_load, Schema

from models import Cohort


class CohortSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()
    nickname = fields.String()
    duration = fields.Integer()
    start_date = fields.Date()
    is_active = fields.Boolean(allow_none=True)
    review_schema = fields.Dict(allow_none=True)
    feedback_schema = fields.Dict(allow_none=True)

    @post_load
    def make_cohort(self, data, **kwargs):
        return Cohort(**data)
