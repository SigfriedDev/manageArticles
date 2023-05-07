import logging
from typing import List
import json
import re

from src.manage.exceptions.categories_exceptions import CategoriesError

from ..dto import (
    CreateCategoryInputSchema,
    CreateCategoryOutputSchema,

    getAllCategoryOutputSchema,
    allCategorySchema 

)

from ..model.categories import Categories

class CategoryService:
    def create(request: CreateCategoryInputSchema) -> CreateCategoryOutputSchema:
        newCategory: Categories = Categories.create(**request)
        if not newCategory:
            CategoriesError.notInsert()

        response: CreateCategoryOutputSchema = {}
        response["success"] = True
        response["message"] = "Success to insert a new category"
        response["payload"] = {}
        response["payload"]["id"] = str(newCategory.id)
        return response

    def getAll() -> getAllCategoryOutputSchema:
        response: getAllCategoryOutputSchema = {}
        response["success"] = True
        response["message"] = "Success to get all Categories"
        response["payload"] = []

        categories : Categories = Categories.find()

        if not categories:
            response

        arrayCategories: list[allCategorySchema] = []

        for category in categories:
            newCategory: allCategorySchema = {}
            newCategory["id"] = str(category.id)
            newCategory["name"] = str(category.name)
         
            arrayCategories.append(newCategory)

        if arrayCategories != []:
            response["payload"] = arrayCategories
        return response


    def allCategoriesArticles(allArticlesList):

        arrayArticles: List[allArticlesList] = []

        for article in allArticlesList:
            newArticle: allArticlesList = {}
            newArticle["id"] = str(article.id)
            newArticle["title"]=str(article.title)
            newArticle["text"] = article.text
            newArticle["publishDate"] = str(article.publishDate)
            newArticle["categories"] = []
  


            if article.category:

                listCategories = CategoryService.categoryArticle(
                    article.category
                )


                newArticle["categories"] = listCategories

            arrayArticles.append(newArticle)

        return arrayArticles

    def categoryArticle(articleList):
        listCategories = []

        for category in articleList:
            
            category = Categories.find_one(id=category.category_id, active = True)

            if category:

                category.name = str(category.name)

                del category.id
                del category.article
                del category.startAt
                del category.deleteAt
                del category.updateAt
                del category.active
                del category._sa_instance_state

                listCategories.append(category.__dict__)

        return listCategories

