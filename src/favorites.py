from models import Favorites, db
from sqlalchemy.exc import SQLAlchemyError


def get_favorites_by_user(user_id):
    try:
        favorites = Favorites.query.filter_by(user_id=user_id).all()
        return [favorite.serialize() for favorite in favorites]
    except SQLAlchemyError as e:
        raise Exception(f"Error retrieving favorites: {str(e)}")

def add_favorite(user_id, favorite_type, favorite_id):
    try:
        new_favorite = Favorites(user_id=user_id, favorite_type=favorite_type, favorite_id=favorite_id)
        db.session.add(new_favorite)
        db.session.commit()
        return {"message": f"{favorite_type.capitalize()} added to favorites"}
    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Error adding favorite: {str(e)}")


def delete_favorite(user_id, favorite_type, favorite_id):
    try:
        favorite = Favorites.query.filter_by(user_id=user_id, favorite_type=favorite_type, favorite_id=favorite_id).first()
        if not favorite:
            return None
        db.session.delete(favorite)
        db.session.commit()
        return {"message": "Favorite deleted"}
    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Error deleting favorite: {str(e)}")

