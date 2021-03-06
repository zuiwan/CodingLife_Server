#!/usr/bin/env python
# -*- coding: utf-8 -*-
from marshmallow import Schema, fields, post_load
from Library.extensions import orm

from Library.OrmModel import BaseModel, BaseSchema
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

SECRET_KEY = 'the quick brown fox jumps over the lazy dog'


class UserSchema(BaseSchema):
    name = fields.Str()
    email = fields.Str()
    level = fields.Int()

    @post_load
    def make_user(self, data):
        return User(**data)


class User(BaseModel):
    schema = UserSchema(strict=True)
    default_level = 0

    name = orm.Column(orm.String(32), index=True)
    phone = orm.Column(orm.String(32), default="")
    level = orm.Column(orm.Integer, default=default_level)
    password_hash = orm.Column(orm.String(500), default="")

    def __init__(self,
                 name,
                 phone=None,
                 level=None,
                 id=None):
        self.name = name
        self.phone = phone
        self.level = level
        if id is None:
            self.id = id

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=1000):
        s = Serializer(SECRET_KEY, expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            raise  # invalid token
        user = User.query.get(data['id'])
        return user

    @staticmethod
    def verify_admin_temp_token(token):
        s = Serializer(SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            raise  # invalid token
        user = User.query.get(data['id'])
        return user

    @property
    def username(self):
        return self.name
