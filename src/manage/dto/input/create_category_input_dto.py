from marshmallow import Schema, fields, ValidationError

class CreateCategoryInputSchema(Schema):
    name = fields.String(required=True, description="Name of category", example="History")

    class Meta:
        ordered = True
class CreateCategoryInput:
    def create(body: CreateCategoryInputSchema):
        try:
            return CreateCategoryInputSchema().load(body)
        except ValidationError as err:
            raise Exception(err)