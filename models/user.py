from sqlalchemy import Column, Boolean, Integer, String
from sqlalchemy.orm.exc import NoResultFound
from lib.db import BaseModel, Model, session_factory

class User(BaseModel, Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String)
    slack = Column(String)
    is_active = Column(Boolean)
    is_busy = Column(Boolean)

    @staticmethod
    def set_active(name, active):
        with session_factory() as sess:
            try:
                user = sess.query(User).filter(
                    User.slack==name
                ).one()
                user.is_active = active
                user.save()
                return True
            except NoResultFound:
                return False

    @staticmethod
    def set_busy(name, busy):
        with session_factory() as sess:
            try:
                user = sess.query(User).filter(
                    User.slack==name
                ).one()
                user.is_busy = busy
                user.save()
                return True
            except NoResultFound:
                return False

    @staticmethod
    def is_mentor(name):
        with session_factory() as sess:
            try:
                sess.query(User).filter(
                    User.slack==name,
                ).one()
                return True
            except NoResultFound:
                return False