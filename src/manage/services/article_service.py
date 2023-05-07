import logging
from typing import List
import json
import re

from src.manage.exceptions.articles_exceptions import ArticlesError
from ..services.category_service import (
    CategoryService
)
from ..dto import (
    CreateArticleInputSchema,
    CreateArticleOutputSchema,
    allArticlesSchema,
    getAllArticlesOutputSchema,
    deleteArticleInputSchema,
    deleteArticleInput,
    deleteArticleOutputSchema
)

from ..model import (
    Articles, 
    ArticlesCategories
)
from ..utils.validate_attribute import validateAttribute
class ArticleService:
    def create(request: CreateArticleInputSchema) -> CreateArticleOutputSchema:

        request=dict(request)

        exist: Articles = Articles.find_one(title = request["title"])
             
        if exist:
            ArticlesError.exist()

        newArticle: Articles = Articles.create(title = request["title"], text=str(request["text"]), author=request["author"], publishDate=request["publishDate"])

        if validateAttribute(request, 'category_id'): 
            for dato in request['category_id']:
                print("entro")
                asignCategory: ArticlesCategories = ArticlesCategories.create(articles_id = str(newArticle.id), category_id = str(dato))
        
        response: CreateArticleOutputSchema = {}
        response["success"] = True
        response["message"] = "Success to insert a new article"
        response["payload"] = {}
        response["payload"]["id"] = str(newArticle.id)
        return response
    

    def getAll() -> getAllArticlesOutputSchema:

        articles: List[Articles] = Articles.find(active=True)


        if not Articles:
            ArticlesError.notFound()
        arrayArticles: List[allArticlesSchema] = []
        
        arrayArticles = CategoryService.allCategoriesArticles(articles)
        
        response: getAllArticlesOutputSchema = {}
        response["success"] = True
        response["message"] = "Success to get all Articles"
        response["payload"] = arrayArticles

        return response

    
    def delete(request: deleteArticleInputSchema):
        exist: Articles = Articles.find_one(id=request["id"], active=True)

        if not exist:
            ArticlesError.notFound()

        delete: int = Articles.delete(id=request["id"], active=True)

        if not delete:
            ArticlesError.notDelete()

        response: deleteArticleOutputSchema = {}
        response["success"] = True
        response["message"] = "Success to deleted article"
        response["payload"] = {}
        response["payload"]["id"] = str(request["id"])
        return response
