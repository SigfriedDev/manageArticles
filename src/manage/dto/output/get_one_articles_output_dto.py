from marshmallow import Schema, fields, ValidationError


class CreateArticleBodySchema(Schema):

    id = fields.UUID(required=True, description="0530e7f1-ca47-4067-9543-b19046953ef1")
    title = fields.UUID(required=True, description="Title of article")
    author = fields.UUID(required=True, description="Description of article")
    publishDate = fields.String(required=False, description="Date of publish the article")
    category = fields.Raw()

class CreateArticleOutputSchema(Schema):
    success = fields.Boolean(
        required=True, description="If this field is true, the operation is correctly"
    )
    message = fields.String(required=True, description="User insert correctly")
    payload = fields.Nested(
            CreateArticleBodySchema(), required=True, description="Payload response"
        )
    

    class Meta:
        ordered = True


class CreateArticleOutput:
    def create(input: CreateArticleOutputSchema):
        try:
            return CreateArticleOutputSchema().load(input)
        except ValidationError as err:
            raise Exception(err)