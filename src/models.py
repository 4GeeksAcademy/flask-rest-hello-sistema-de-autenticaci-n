from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=True)
    planets_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=True)
    startships_id = db.Column(db.Integer, db.ForeignKey('startships.id'), nullable=True)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return '<Favorites %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "people_id": self.people_id,
            "planets_id": self.planets_id,
            "starships_id": self.startships_id,
            "users_id": self.users_id,
        }

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable = False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '<Users %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable = False)
    eye_color = db.Column(db.String(250), nullable=False)
    height = db.Column(db.Integer, nullable=False)
    people_favorites = db.relationship(Favorites)

    def __repr__(self):
        return '<People %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "eye_color": self.eye_color,
            "height": self.height
        }
    
class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable = False)
    climate = db.Column(db.String(250), nullable=False)
    population = db.Column(db.Integer, nullable=False)
    planets_favorites = db.relationship(Favorites)

    def __repr__(self):
        return '<Planets %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "population": self.population
        }

class Startships(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable = False)
    model = db.Column(db.String(250), nullable=False)
    passengers = db.Column(db.Integer, nullable=False)
    startships_favorites = db.relationship(Favorites)

    def __repr__(self):
        return '<Startships %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "passengers": self.passengers
        }
