from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from sqlalchemy import exc
from sqlalchemy.orm import relationship
from ..connection import db, session

class Categories(db):

    __tablename__ = "categories"
    id = Column(UUID(as_uuid=True), primary_key=True, default=lambda: uuid4().hex)
    name = Column(String(100), nullable=False)
    article = relationship(
        "ArticlesCategories", back_populates="article", lazy="joined"
    )


    startAt = Column(DateTime, default=datetime.now)
    updateAt = Column(DateTime)
    deleteAt = Column(DateTime)
    active = Column(Boolean, default=True)

    def find(**kwargs):
        try:
            return session.query(Categories).filter_by(**kwargs).all()
        except exc.SQLAlchemyError as err:
            print(err)
            return {}
        finally:
            session.close()

    def find_one(**kwargs):
        try:
            return session.query(Categories).filter_by(**kwargs).first()
        except exc.SQLAlchemyError as err:
            print(err)
            return {}
        finally:
            session.close()

    def create(**request):
        try:       
            category = Categories(**request)
            session.add(category)
            session.commit()
            return category
        except exc.SQLAlchemyError as err:
            print(err)
            session.rollback()
            return {}