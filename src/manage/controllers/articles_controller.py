from flask.views import MethodView
from flask_smorest import Blueprint
from flask import jsonify, request, render_template, redirect, url_for
from json import JSONEncoder, dumps

from ..dto import (
    CreateArticleInputSchema,
    CreateArticleOutputSchema,
    CreateArticleInput,
    CreateArticleOutput,

    getAllArticlesOutputSchema,
    getAllArticlesOutput,

    deleteArticleInput,
    deleteArticleInputSchema,
    deleteArticleOutputSchema,
    deleteArticleOutput

)
from ..services.article_service import ArticleService
from ..services.category_service import CategoryService

article = Blueprint(
    "Article", "Article", url_prefix="/article/", description="Article"
)


class Article(MethodView):
    @article.errorhandler(404)
    def controlled_errors(e):
        return (
            jsonify(code=404, errors=e.description, message="API error", status="API"),
            404,
        )

    @article.errorhandler(Exception)
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

    @article.route("/create", methods=["POST", "GET"])
    def addarticle(): #
        """Create article"""
        if request.method == 'POST':
            body = {}
            body["title"] = request.form['title']
            body["text"] = request.form['text']
            body["author"] = request.form['author']
            body["publishDate"] = request.form['publishDate']
            body["category_id"] = request.form.getlist('categories[]')
            body: CreateArticleInputSchema = CreateArticleInput.create(body)
            response = ArticleService.create(body)
            return CreateArticleOutput.create(response)
        else:
            categories = CategoryService.getAll()
            return render_template('add_article.html', categories=categories["payload"])


    @article.route("/get", methods=["GET"])
    @article.response(
        200, getAllArticlesOutputSchema, content_type="application/json"
    )
    @article.doc(authorize=True)
    def get():
        """Get All articles"""
        response = ArticleService.getAll()
        return getAllArticlesOutput.create(response)


    @article.route("/delete/<id>", methods=["POST"])
    @article.response(
        200, deleteArticleOutputSchema, content_type="application/json"
    )
    @article.doc(authorize=True)
    def delete(id):
        """Delete article"""
        if request.method == 'POST':
            body = {}
            body["id"] = id
            body: deleteArticleInputSchema = deleteArticleInput.create(body)
            response = ArticleService.delete(body)
            return deleteArticleOutput.create(response)
        else:
            return redirect(url_for('Article.delete'))
