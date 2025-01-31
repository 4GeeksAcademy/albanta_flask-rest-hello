from models import Planets  
from sqlalchemy.exc import SQLAlchemyError

def get_all_planets():
    try:
        planets = Planets.query.all()  
        return [planet.serialize() for planet in planets]
    except SQLAlchemyError as e:
        raise Exception(f"Error retrieving planets: {str(e)}")

def get_planet_by_id(planet_id):
    try:
        planet = Planets.query.get(planet_id)  
        if not planet:
            return None
        return planet.serialize()
    except SQLAlchemyError as e:
        raise Exception(f"Error retrieving planet: {str(e)}")
