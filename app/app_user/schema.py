from app.extension.modules import ma
from flask import url_for
from marshmallow import fields


class UserSchema(ma.Schema):
    # class Meta:
        # fields = ("id", "username" , "dll")
    id = fields.Integer()
    username = fields.String()
    email = fields.String()
    profile = fields.Method('get_display_profile')


    def get_display_profile(self,info):
        if info.profile:
            return url_for('static', filename='' + info.profile)
