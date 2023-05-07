from marshmallow import Schema, fields, ValidationError


class allArticlesSchema(Schema):

    id = fields.String(required=True, description="Category UUID")
    title = fields.String(
        required=True, description="Title of article"
    )
    text = fields.String(
        required=True, description="Text of Article"
    )
    publishDate = fields.String(required=True, description="Publish Date")
    categories = fields.Raw()

class getAllArticlesOutputSchema(Schema):
    success = fields.Boolean(
        required=True, description="If this field is true, the operation is correctly"
    )
    message = fields.String(required=True, description="Message action")
    payload = fields.List(
        fields.Nested(
            allArticlesSchema(), required=True, description="Payload response"
        )
    )

    class Meta:
        ordered = True


class getAllArticlesOutput:
    def create(input: getAllArticlesOutputSchema):
        try:
            return getAllArticlesOutputSchema().load(input)
        except ValidationError as err:
            raise Exception(err)