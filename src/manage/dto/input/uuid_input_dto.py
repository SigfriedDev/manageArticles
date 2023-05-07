from marshmallow import Schema, ValidationError, fields


class UuidInputSchema(Schema):

    id = fields.UUID(required=True, description="Send a validate ID")

    class Meta:
        ordered = True


class UuidInput:
    def create(body: UuidInputSchema):
        try:
            return UuidInputSchema().load(body)
        except ValidationError as err:
            raise Exception(err)