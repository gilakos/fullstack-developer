#!/usr/bin/env python3

# Import libraries
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

# Create instance of base class
Base = declarative_base()


class Restaurant(Base):
    '''
    Table class for restaurant info
    '''
    __tablename__ = 'restaurant'

    # id Column is Primary
    id = Column(Integer, primary_key=True)
    # name of restaurant, can't be null
    name = Column(String(250), nullable=False)


# Instantiate engine
engine = create_engine('sqlite:///restaurantmenu.db')

# Create the database
Base.metadata.create_all(engine)
