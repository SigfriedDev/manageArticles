from marshmallow import Schema, fields, ValidationError


class deleteArticleSchema(Schema):
    id = fields.String(required=True, description="UUID to Article deleted")

    class Meta:
        ordered = True


class deleteArticleOutputSchema(Schema):
    success = fields.Boolean(
        required=True, description="If this field is true, the operation is correctly"
    )
    message = fields.String(required=True, description="Message action")
    payload = fields.Nested(
        deleteArticleSchema(), required=True, description="Payload response"
    )

    class Meta:
        ordered = True


class deleteArticleOutput:
    def create(input: deleteArticleOutputSchema):
        try:
            return deleteArticleOutputSchema().load(input)
        except ValidationError as err:
            raise Exception(err)
