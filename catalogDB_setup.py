#!/usr/bin/env python

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
Base = declarative_base()

class User(Base):
    # Same User Class as presented in oauth course
    __tablename__ = 'user'

    name =Column(String(250), nullable = False)
    id = Column(Integer, primary_key = True)
    email = Column(String(250), nullable = False)
    picture = Column(String(250))
    
    @property
    def serialize(self):
       return {
           'name'         : self.name,
           'id'         : self.id,
           'email'         : self.email,
           'picture'         : self.picture,
       }

# These are store item categories
class Category(Base):
    __tablename__ = 'category'
   
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer,ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
       return {
           'name'         : self.name,
           'id'           : self.id,
           'user_id'    : self.user_id,

       }

# These are store items themselves
class Item(Base):
    __tablename__ = 'store_item'

    name =Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(250))
    price = Column(String(8))
    category_id = Column(Integer,ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
       return {
           'name'         : self.name,
           'description'         : self.description,
           'id'         : self.id,
           'price'         : self.price,
           'user_id'     : self.user_id,
           'category_id' : self.category_id,
           'category' : self.category
       }



engine = create_engine('sqlite:///catalog-db.db')
 

Base.metadata.create_all(engine)