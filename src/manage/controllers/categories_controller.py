from flask.views import MethodView
from flask_smorest import Blueprint
from flask import jsonify, request, url_for
from json import JSONEncoder, dumps

from ..dto import (
    CreateCategoryInputSchema,
    CreateCategoryOutputSchema,
    CreateCategoryInput,
    CreateCategoryOutput,

    getAllCategoryOutput,
    getAllCategoryOutputSchema

)
from ..services.category_service import CategoryService


category = Blueprint(
    "Category", "Category", url_prefix="/category/", description="Category"
)


class Category(MethodView):
    @category.errorhandler(404)
    def controlled_errors(e):
        return (
            jsonify(code=404, errors=e.description, message="API error", status="API"),
            404,
        )

    @category.errorhandler(Exception)
    def general_exception(e):
        try:
            return (
                jsonify(
                    code=402,
                    errors=e.data["messages"]["json"],
                    message="API error",
                    status="API",
                ),
                422,
            )
        except:
            return (
                jsonify(code=402, errors=str(e), message="API error", status="API"),
                422,
            )

    @category.route("/create", methods=["POST"])
    @category.arguments(CreateCategoryInputSchema, location="json")
    @category.response(
        200, CreateCategoryOutputSchema, content_type="application/json"
    )
    def addCategory(body: CreateCategoryInputSchema):
        """Create category"""
        print(body)
        body: CreateCategoryInputSchema = CreateCategoryInput.create(body)
        response = CategoryService.create(body)
        return CreateCategoryOutput.create(response)
    
    @category.route("/get", methods=["GET"])
    @category.response(
        200, getAllCategoryOutputSchema, content_type="application/json"
    )
    @category.doc(authorize=True)
    def get():
        """Get All categories"""
        response = CategoryService.getAll()
        return getAllCategoryOutput.create(response)

    # @article.route("/get/<id>", methods=["GET"])
    # @article.arguments(UuidInputSchema, location="path", as_kwargs=True)
    # @article.response(
    #     200, getOneArticleOutputSchema, content_type="application/json"
    # )
    # def getById(id: str):
    #     """Get a article by ID"""
    #     id: str = str(id)
    #     response =ArticleService.get(id)

    #     return getOneArticleOutput.create(response)

