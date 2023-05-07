from marshmallow import Schema, fields, ValidationError


class CreateCategoryBodySchema(Schema):

    id = fields.UUID(required=True, description="0530e7f1-ca47-4067-9543-b19046953ef1")


class CreateCategoryOutputSchema(Schema):
    success = fields.Boolean(
        required=True, description="If this field is true, the operation is correctly"
    )
    message = fields.String(required=True, description="Category insert correctly")
    payload = fields.Nested(
            CreateCategoryBodySchema(), required=True, description="Payload response"
        )
    

    class Meta:
        ordered = True


class CreateCategoryOutput:
    def create(input: CreateCategoryOutputSchema):
        try:
            return CreateCategoryOutputSchema().load(input)
        except ValidationError as err:
            raise Exception(err)