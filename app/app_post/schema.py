import moment
from app.app_user.schema import UserSchema
from app.extension.modules import ma
from marshmallow import fields


class PostSchema(ma.Schema):
    id = fields.String()
    content = fields.String()
    create_at = fields.Method('get_create_at_display')
    author = fields.Nested(UserSchema)

    def get_create_at_display(self,info):
        if info.create_at:
            return moment.date(info.create_at).strftime("%d-%m-%Y")
