from extensions.extension import (
    Model,
    String,
    Integer,
    Column,
    DateTime,
    ForeignKey,
    relationship,
)
from extensions.extension import db
from sqlalchemy.sql import func
from sqlalchemy.exc import InvalidRequestError, IntegrityError, ProgrammingError


class Users(Model):
    __tablename__ = "users"

    id = Column(Integer(), autoincrement=True, primary_key=True)
    first_name = Column(String(), nullable=False)
    last_name = Column(String(), nullable=False)
    user_name = Column(String(), nullable=False)
    email = Column(String(), nullable=False, unique=True)
    password = Column(String(), nullable=False)
    todos = relationship("Todo")
    created = Column(DateTime(timezone=True), default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    def save_db(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except (InvalidRequestError, ProgrammingError, IntegrityError) as err:
            print(err)
            db.session.remove()
            return False

    def update(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

        return self.save_db()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

        return True


class Todo(Model):
    __tablename__ = "todos"

    id = Column(Integer(), autoincrement=True, primary_key=True)
    title = Column(String(), nullable=False)
    description = Column(String())
    created = Column(DateTime(timezone=True), default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    user_id = Column(
        Integer(), ForeignKey("users.id", use_alter=True, ondelete="SET NULL")
    )

    def save_db(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except (InvalidRequestError, ProgrammingError, IntegrityError):
            db.session.remove()
            return False

    def update(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

        return self.save_db()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

        return True
