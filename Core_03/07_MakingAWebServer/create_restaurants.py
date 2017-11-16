#!/usr/bin/env python3

# Import libraries
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from create_db import Base, Restaurant

# Instantiate engine
engine = create_engine('sqlite:///restaurantmenu.db')

# Bind engine to Bass class
Base.metadata.bind = engine
# Create sessionmaker object
DBSession = sessionmaker(bind = engine)
# Interface for sqlalchemy commands (staging zone)
session = DBSession()

# Define new entries
session.add(Restaurant(name = "Urban Burger"))
session.add(Restaurant(name = "Panda Garden"))
session.add(Restaurant(name = "Thyme for That Vegetarian Cuisine"))
session.add(Restaurant(name = "Tony's Bistro"))
session.add(Restaurant(name = "Andala's"))
session.add(Restaurant(name = "Auntie Ann's Diner"))
session.add(Restaurant(name = "Cocina Y Amor"))

# Commit changes to the db
session.commit()

# Test database query
session.query(Restaurant).all()