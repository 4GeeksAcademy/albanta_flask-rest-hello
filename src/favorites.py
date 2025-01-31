from models import Favorites, Planets, People, db  

def get_favorites_by_user(user_id):
    try:
        favorites = Favorites.query.filter_by(user_id=user_id).all() 
        return [favorite.serialize() for favorite in favorites]
    except SQLAlchemyError as e:
        raise Exception(f"Error retrieving favorites: {str(e)}")

def add_favorite(user_id, planet_id=None, people_id=None):
    try:
        if planet_id:
            planet = Planets.query.get(planet_id)  
            if not planet:
                return {"error": "Planet not found"}
            new_favorite = Favorites(user_id=user_id, planet_id=planet_id)  

        elif people_id:
            person = People.query.get(people_id)
            if not person:
                return {"error": "Character not found"}
            new_favorite = Favorites(user_id=user_id, people_id=people_id)  

        else:
            return {"error": "Must provide either planet_id or people_id"}

        db.session.add(new_favorite)
        db.session.commit()
        return {"message": "Favorite added successfully"}

    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Error adding favorite: {str(e)}")

def delete_favorite(user_id, planet_id=None, people_id=None):
    try:
        if planet_id:
            favorite = Favorites.query.filter_by(user_id=user_id, planet_id=planet_id).first()  
        elif people_id:
            favorite = Favorites.query.filter_by(user_id=user_id, people_id=people_id).first()  
        else:
            return {"error": "Must provide either planet_id or people_id"}

        if not favorite:
            return {"error": "Favorite not found"}

        db.session.delete(favorite)
        db.session.commit()
        return {"message": "Favorite deleted"}

    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Error deleting favorite: {str(e)}")
