from models import User
from sqlalchemy.exc import SQLAlchemyError


def get_all_users():
    try:
        users = User.query.all()
        return [user.serialize() for user in users]
    except SQLAlchemyError as e:
        raise Exception(f"Error retrieving users: {str(e)}")
