from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from sqlalchemy import exc
from sqlalchemy.orm import relationship
from ..connection import db, session

class Articles(db):

    __tablename__ = "articles"
    id = Column(UUID(as_uuid=True), primary_key=True, default=lambda: uuid4().hex)
    title = Column(String(100), nullable=False)
    text = Column(String(60000))
    author = Column(String(80))
    publishDate = Column(DateTime)

    category = relationship(
        "ArticlesCategories", back_populates="category", lazy="joined"
    )

    startAt = Column(DateTime, default=datetime.now)
    updateAt = Column(DateTime)
    deleteAt = Column(DateTime)
    active = Column(Boolean, default=True)

    def find(**kwargs):
        try:
            return session.query(Articles).filter_by(**kwargs).all()
        except exc.SQLAlchemyError as err:
            print(err)
            return {}
        finally:
            session.close()

    def find_one(**kwargs):
        try:
            return session.query(Articles).filter_by(**kwargs).first()
        except exc.SQLAlchemyError as err:
            print(err)
            return {}
        finally:
            session.close()

    def create(**request):
        try:       
            article = Articles(**request)
            session.add(article)
            session.commit()
            return article
        except exc.SQLAlchemyError as err:
            print(err)
            session.rollback()
            return {}


    def delete(**kwargs) -> int:
        try:         
            updated = (
                session.query(Articles)
                .filter_by(**kwargs)
                .update(
                    {"active": False, "deleteAt": datetime.now()},
                    synchronize_session="fetch",
                )
            )
            session.commit()
            return updated
        except exc.SQLAlchemyError as err:
            print(err)
            session.rollback()
            return {}
        