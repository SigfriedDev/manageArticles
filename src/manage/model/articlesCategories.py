from datetime import datetime
from sqlalchemy import Column, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4
from ..connection import db, session
from sqlalchemy import exc


class ArticlesCategories(db):

    __tablename__ = "articlesCategories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=lambda: uuid4().hex)
    articles_id = Column(UUID(as_uuid=True), ForeignKey("articles.id"), primary_key=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), primary_key=False)

    category = relationship("Articles", back_populates="category", lazy="joined")
    article = relationship("Categories", back_populates="article", lazy="joined")
    
    startAt = Column(DateTime, default=datetime.now)
    deleteAt = Column(DateTime)
    active = Column(Boolean, default=True)

    def find():
        try:
            return session.query(ArticlesCategories).filter_by(active=True).all()
        except exc.SQLAlchemyError as err:
            print(err)
            return {}
        finally:
            session.close()

    def find_one(**kwargs):
        try:
            return session.query(ArticlesCategories).filter_by(**kwargs).first()
        except exc.SQLAlchemyError as err:
            print(err)
            return {}
        finally:
            session.close()

    def create(**request):
        try:
            newArticleCategory = ArticlesCategories(**request)
            session.add(newArticleCategory)
            session.commit()
            return newArticleCategory
        except exc.SQLAlchemyError as err:
            print(err)
            session.rollback()
            return {}
    
    
    def delete(**kwargs) -> int:
        try:
            updated = session.query(ArticlesCategories).filter_by(**kwargs).delete()
            session.commit()
            return updated
        except exc.SQLAlchemyError as err:
            print(err)
            session.rollback()
            return {}
        