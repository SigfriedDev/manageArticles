from marshmallow import Schema, fields, ValidationError

class responseSchema(Schema):
    starting = fields.String(required=True)
    name = fields.String(required=True)
    version = fields.String(required=True)

    class Meta:
        ordered = True

class mainOutput:
    def __init__(self, input: responseSchema):
        self.input = input

    def create(self):
        try:
            return responseSchema().load(self.input)
        except ValidationError as err:
            raise Exception(err)
