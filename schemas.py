from marshmallow import Schema, fields #fields allow us to specify info we need coming in and out and the datatyp

#marshmallow schemas = group of classes that helps validate info coming into one of our routes/requests



class PostSchema(Schema):
    id = fields.Str(dump_only=True) #serializes data as info gets sent back, dumps only = not required when receiving a post only when sending
    name = fields.Str(required=True) #required = true, user input required
    location = fields.Str(required=True)
    highlights = fields.List(fields.Str(), required=True)
    user_id = fields.Int(required=True)
    timestamp = fields.Str(dump_only=True)
    #user = fields.List(fields.Nested(UserSchema()), dump_only=True)


class UserSchema(Schema):
    id = fields.Str(dump_only=True) #dumps_only=True --> not expecting an id but will send one back
    username = fields.Str(required=True) 
    email = fields.Str(required=True) 
    password = fields.Str(required=True, load_only=True) #load_only=True --> expecting an id/password but will never send one back
    first_name = fields.Str() #requesting name from user but user input is optional
    last_name = fields.Str()
  

class UserSchemaNested(UserSchema): #inherits from UserSchema
    posts = fields.List(fields.Nested(PostSchema), dump_only=True)
    followed = fields.List(fields.Nested(UserSchema), dump_only=True)


class UpdateUserSchema(Schema): #don't need id here because we're not sending user schema
    username = fields.Str() #optional not required, user may send us username to update
    email = fields.Str()
    password = fields.Str(required=True, load_only=True)
    new_passworld = fields.Str()
    name = fields.Str() 
    location = fields.Str()
    highlights = fields.List(fields.Str())
    first_name = fields.Str() #requesting name from user but user input is optional
    last_name = fields.Str() 


class DeleteUserSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)