from sqlalchemy.exc import IntegrityError

from marshmallow import fields
from marshmallow import validates
from marshmallow import ValidationError

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
        try:
            user = User(name, email)
            db.session.add(user)
            db.session.commit()
            return user
        except IntegrityError:
            db.session.rollback()
            return

    @classmethod
    def delete_user(cls, user_id):
        user = cls.query.get(user_id)
        db.session.delete(user)
        db.session.commit()

    def update_user(self, name=None, email=None):
        self.name = name if name else self.name
        self.email = email if email else self.email
        db.session.commit()


class UserSchema(ma.Schema):
    name = fields.String(required=True,
                         error_messages={'required': 'Name is required.'})
    email = fields.String(required=True,
                          error_messages={'required': 'Email is required.'})

    class Meta:
        model = User

    @validates('name')
    def validate_name(self, name):
        if User.query.filter_by(name=name).first():
            raise ValidationError(f'User with name {name} already exists')

    @validates('email')
    def validate_email(self, email):
        if User.query.filter_by(email=email).first():
            raise ValidationError(f'User with email {email} already exists')
