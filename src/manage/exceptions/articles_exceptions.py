from . import Error


class ArticlesError:
    def notInsert():
        Error("Article not Inserted")
    
    def notFound():
        Error("Article not found")

    def exist():
        Error("Article exist")

    def notDelete():
        Error("Article not deleted")
