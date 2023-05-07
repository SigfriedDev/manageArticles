from flask.views import MethodView
from flask_smorest import Blueprint
from flask import jsonify, render_template
from ..services.article_service import ArticleService


main = Blueprint("Main", "main", url_prefix="/", description="Main")


class Main(MethodView):
    @main.route("/", methods=["GET"])
    def index():
        articles = ArticleService.getAll()
        return render_template('index.html', articles=articles["payload"])
        
