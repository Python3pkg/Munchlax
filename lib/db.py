from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager
from .secrets import secrets

eng = 'sqlite:///{path}'.format(**secrets.db.__dict__)
engine = create_engine(eng)

factory = sessionmaker(bind=engine)
Session = scoped_session(factory)
BaseModel = declarative_base()

@contextmanager
def session_factory():
    s = Session()

    try:
        yield s
        s.commit()
    except:
        s.rollback()
        raise
    finally:
        s.close()

class Model():
    __tablename__ = None

    def save(self):
        with session_factory() as sess:
            sess.merge(self)

    def delete(self):
        with session_factory() as sess:
            sess.delete(self)
