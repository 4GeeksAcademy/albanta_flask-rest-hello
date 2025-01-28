from models import People
from sqlalchemy.exc import SQLAlchemyError


def get_all_people():
    try:
        people = People.query.all()
        return [person.serialize() for person in people]
    except SQLAlchemyError as e:
        raise Exception(f"Error retrieving people: {str(e)}")

def get_person_by_id(people_id):
    try:
        person = People.query.get(people_id)
        if not person:
            return None
        return person.serialize()
    except SQLAlchemyError as e:
        raise Exception(f"Error retrieving person: {str(e)}")
