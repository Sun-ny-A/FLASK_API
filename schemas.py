from marshmallow import Schema, fields #fields allow us to specify info we need coming in and out and the datatyp

#marshmallow schemas = group of classes that helps validate info coming into one of our routes/requests

class PostSchema(Schema):
    id = fields.Str(dumps_only=True) #serializes data as info gets sent back, dumps only = not required when receiving a post only when sending
    name = fields.Str(required=True) #required = true, user input required
    location = fields.Str(required=True)
    highlights = fields.List(fields.Str(), required=True)
    user_id = fields.Str(required=True)


class UserSchema(Schema):
    id = fields.Str(dumps_only=True)
    username = fields.Str(required=True) 
    email = fields.Str(required=True) 
    password = fields.Str(required=True)
    first_name = fields.Str() #requesting name from user but user input is optional
    last_name = fields.Str() 


class UpdateUserSchema(Schema): #don't need id here because we're not sending user schema
    username = fields.Str() #optional not required, user may send us username to update
    email = fields.Str()
    password = fields.Str(required=True)
    new_passworld = fields.Str()
    name = fields.Str() 
    location = fields.Str()
    highlights = fields.List(fields.Str())
    first_name = fields.Str() #requesting name from user but user input is optional
    last_name = fields.Str() 