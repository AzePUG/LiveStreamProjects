from extensions.extension import Model,String,Integer,Column,DateTime
from extensions.extension import db
from sqlalchemy.sql import func


class Users(Model):
    __tablename__ = "users"

    id = Column(Integer(),autoincrement=True,primary_key=True)
    first_name = Column(String(),nullable=False)
    last_name = Column(String(),nullable=False)
    user_name = Column(String(),nullable=False)
    email = Column(String(),nullable=False)
    password = Column(String(),nullable=False)
    created = Column(DateTime(timezone=True), default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now(),nullable=True)

    def save_db(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self,**kwargs):
        for key,val in kwargs.items():
            setattr(self,key,val)

        return self.save_db()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
        return True