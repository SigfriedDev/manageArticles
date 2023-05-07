from marshmallow import Schema, fields, ValidationError

class categorySchema(Schema):
    category_id = fields.String(required=True, description="Id of the category for article")


class CreateArticleInputSchema(Schema):
    title = fields.String(required=True, description="Title of article", example="History Article")
    text = fields.String(required=True, description="Text of article")
    author = fields.String(required=True, description="Article author", example="Octavio Paz")
    publishDate = fields.String(required=False, description="Date of publish article")
    # category_id = fields.String(required=True, description="Id of the category for article")

    category_id = fields.List(fields.String(), required=False)
    
    class Meta:
        ordered = True
class CreateArticleInput:
    def create(body: CreateArticleInputSchema):
        try:
            return CreateArticleInputSchema().load(body)
        except ValidationError as err:
            raise Exception(err)