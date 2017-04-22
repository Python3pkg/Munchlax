from sqlalchemy import Column, Integer, String
from sqlalchemy.orm.exc import NoResultFound
from lib.db import BaseModel, Model, session_factory

class User(BaseModel, Model):
    __tablename__ = 'bookmark_instances'

    id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String)
    slack = Column(String)
    is_active = Column(Integer)
    is_busy = Column(Integer)

    @staticmethod
    def set_active(id, active):
        with session_factory() as sess:
            try:
                user = sess.query(User).filter(
                    User.slack==id
                ).one()
                user.is_active = active
                user.save()
                return True
            except NoResultFound:
                return False

    @staticmethod
    def set_busy(id, busy):
        with session_factory() as sess:
            try:
                user = sess.query(User).filter(
                    User.slack==id
                ).one()
                user.is_busy = busy
                user.save()
                return True
            except NoResultFound:
                return False