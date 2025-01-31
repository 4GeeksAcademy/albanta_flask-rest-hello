from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):  
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    is_active = db.Column(db.Boolean(), nullable=False)

    favorites = db.relationship("Favorites", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }

class People(db.Model):  
    __tablename__ = 'people'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    height = db.Column(db.String(10), nullable=True)
    mass = db.Column(db.String(10), nullable=True)
    hair_color = db.Column(db.String(20), nullable=True)
    skin_color = db.Column(db.String(20), nullable=True)
    eye_color = db.Column(db.String(20), nullable=True)
    birth_year = db.Column(db.String(10), nullable=True)

    favorites = db.relationship("Favorites", back_populates="people", cascade="all, delete-orphan")

    def __repr__(self):
        return f'<People {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
        }

class Planets(db.Model):  
    __tablename__ = 'planets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    climate = db.Column(db.String(50), nullable=False)
    terrain = db.Column(db.String(50), nullable=False)
    population = db.Column(db.Integer, nullable=True)
    diameter = db.Column(db.String(20), nullable=True)
    rotation_period = db.Column(db.String(20), nullable=True)
    orbital_period = db.Column(db.String(20), nullable=True)

    favorites = db.relationship("Favorites", back_populates="planet", cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Planets {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain,
            "population": self.population,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
        }

class Favorites(db.Model):  
    __tablename__ = 'favorites'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=True)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=True)

    user = db.relationship("Users", back_populates="favorites")
    planet = db.relationship("Planets", back_populates="favorites")
    people = db.relationship("People", back_populates="favorites")

    def __repr__(self):
        return f'<Favorites User:{self.user_id} Planet:{self.planet_id} People:{self.people_id}>'

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet": self.planet.serialize() if self.planet else None,
            "people": self.people.serialize() if self.people else None,
        }
