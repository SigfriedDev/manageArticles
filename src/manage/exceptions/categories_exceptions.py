from . import Error


class CategoriesError:
    def notInsert():
        Error("Category not Inserted")
    
    def notFound():
        Error("Category not found")
