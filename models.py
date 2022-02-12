import datetime

from sqlalchemy import Boolean, Column, Date, JSON, SmallInteger, String
from sqlalchemy.orm import validates

from database import Base


class Cohort(Base):
    __tablename__ = 'cohort'
    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    name = Column(String(32), nullable=False)
    nickname = Column(String(16), nullable=False)
    duration = Column(SmallInteger, nullable=False)
    start_date = Column(Date, nullable=False)
    is_active = Column(Boolean, nullable=True)
    review_schema = Column(JSON, nullable=True)
    feedback_schema = Column(JSON, nullable=True)

    @validates('name')
    def validate_name(self, key, name):
        if type(name) is not str:
            raise TypeError

        if len(name) > 32:
            raise ValueError

        return name

    @validates('nickname')
    def validate_nickname(self, key, nickname):
        if type(nickname) is not str:
            raise TypeError

        if len(nickname) > 16:
            raise ValueError

        return nickname

    @validates('duration')
    def validate_duration(self, key, duration):
        if type(duration) is not int:
            raise TypeError

        if duration < 1:
            raise ValueError

        return duration

    @validates('start_date')
    def validate_start_date(self, key, start_date):
        if type(start_date) is not datetime.date:
            raise TypeError

        return start_date

    @validates('is_active')
    def validate_is_active(self, key, is_active):
        if type(is_active) is not bool:
            raise TypeError

        return is_active
