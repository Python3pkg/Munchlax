from sqlalchemy import Column, Boolean, Integer, String
from sqlalchemy.orm.exc import NoResultFound
from lib.db import BaseModel, Model, session_factory

class Request(BaseModel, Model):
    __tablename__ = 'requests'

    id = Column(Integer, primary_key=True)
    requester = Column(String)
    assigned = Column(Integer)
    resolved = Column(Boolean)
    timestamp = Column(String)
    comment = Column(String)
    request = Column(String)

    @staticmethod
    def create(user, timestamp, request):
        with session_factory() as sess:
            Request(
                requester=user,
                assigned=-1,
                resolved=False,
                timestamp=timestamp,
                comment='',
                request=request
            ).save()