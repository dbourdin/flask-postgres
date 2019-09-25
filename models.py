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

    @classmethod
    def delete_user(cls, id):
        user = cls.query.get(id)
        db.session.delete(user)
        db.session.commit()

    def update_user(self, name=None, email=None):
        self.name = name if name else self.name
        self.email = email if email else self.email
        db.session.commit()


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email')
