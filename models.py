from app import db
from app import ma


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return f'<User {self.name}>'

    @classmethod
    def create_user(cls, name, email):
        user = User(name, email)
        db.session.add(user)
        db.session.commit()
        return user


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email')
