# import redis
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

db = SQLAlchemy()
# pool = redis.ConnectionPool(host='127.0.0.1')
# r = redis.Redis(connection_pool=pool)


def session_commit():
    try:
        db.session.commit()
    except SQLAlchemyError as Error:
        db.session.rollback()
        reason = str(Error)
        return reason
