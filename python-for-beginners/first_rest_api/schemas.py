from marshmallow import Schema, fields

# TODO: Validating incoming data

class PlainItemSchema(Schema):
    id = fields.Int(dump_only=True) # dump_only=True: Sending data back to the client
    # These fields are required, and must be in the jSON payload
    name = fields.Str(required=True) 
    price = fields.Float(required=True)

class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()

class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class ItemUpdateSchema(Schema):
    # Not require as it is the update schema
    name = fields.Str()
    price = fields.Float()
    store_id = fields.Int()

class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True) #Whenever we use ItemSchem, we're going to be able to passc in the store_id when we're receiving data from the client
    store = fields.Nested(PlainStoreSchema(), dump_only=True) # Whenever we returning data to the client and not when receiving data from them
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)

class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True) 
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True) 

class TagSchema(PlainTagSchema):
    store_id = fields.Int(load_only=True) 
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)

class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)
