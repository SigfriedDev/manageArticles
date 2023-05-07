from marshmallow import Schema, fields, ValidationError


class allCategorySchema(Schema):

    id = fields.String(required=True, description="Category UUID")
    name = fields.String(
        required=True, description="Name of category"
    )


class getAllCategoryOutputSchema(Schema):
    success = fields.Boolean(
        required=True, description="If this field is true, the operation is correctly"
    )
    message = fields.String(required=True, description="Message action")
    payload = fields.List(
        fields.Nested(
            allCategorySchema(), required=True, description="Payload response"
        )
    )

    class Meta:
        ordered = True


class getAllCategoryOutput:
    def create(input: getAllCategoryOutputSchema):
        try:
            return getAllCategoryOutputSchema().load(input)
        except ValidationError as err:
            raise Exception(err)