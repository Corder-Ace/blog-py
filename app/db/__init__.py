from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
db = SQLAlchemy()


def session_commit():
    try:
        db.session.commit()
    except SQLAlchemyError as Error:
        db.session.rollback()
        reason = str(Error)
        return reason
