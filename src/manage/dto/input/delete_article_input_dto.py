from marshmallow import Schema, ValidationError, fields


class deleteArticleInputSchema(Schema):
    id = fields.UUID(
        required=True, description="add the UUID of the article that you want to delete"
    )

    class Meta:
        ordered = True


class deleteArticleInput:
    def create(body: deleteArticleInputSchema):
        try:
            return deleteArticleInputSchema().load(body)
        except ValidationError as err:
            raise Exception(err)
