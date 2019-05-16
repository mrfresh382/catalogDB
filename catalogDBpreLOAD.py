#!/usr/bin/env python

# This loads the Big Bend Store app with data to view
# This is not required to run the app, but will help test
# OAuth functionality and security. ONLY run this file once.
# If you run multiple times, please delete "catalog-db.db"
# and re-run. 

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from catalogDB_setup import Category, Base, Item, User

engine = create_engine('sqlite:///catalog-db.db')
 
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

User1 = User(name="Smokey the Bear", email="MRsmokeym@gmail.com",
             picture='Bear Pic')
session.add(User1)
session.commit()

category1 = Category(user_id=User1.id, name="Safety Equipment")

session.add(category1)
session.commit()

Item1 = Item(user_id=User1.id, name="Bear Spray", \
	description="We don't allow firearms at the park. Use this to repel dangerous\
	bears", price="$70.50", category= category1)

session.add(Item1)
session.commit()

Item2 = Item(user_id=User1.id, name="Air Horn", \
	description="Toot your horn if you get lost. \
  Someone might hear you.", price="$29.99", category= category1)

session.add(Item2)
session.commit()

Item3 = Item(user_id=User1.id, name="Signal Mirror", \
	description="Use this to signal airplanes or other hikers if you get lost.\
  The park is a no-fly zone for airplanes. Do people still use these?", \
  price="$9.99", category= category1)

session.add(Item3)
session.commit()

User2 = User(name="Ranger Rick", email="BIGrickm@gmail.com",
             picture='Ranger Rick Pic')
session.add(User2)
session.commit()

category2 = Category(user_id=User2.id, name="Hiking Essentials")

session.add(category2)
session.commit()

Item4 = Item(user_id=User2.id, name="Hiking Stick", \
	description="Made from dried up ocotillo plant. Might support your \
  body weight. Made in China", price="$99.99", category= category2)

session.add(Item4)
session.commit()

Item5 = Item(user_id=User2.id, name="M100 Firecracker", \
	description="Due to extremely dry climate, fireworks are strictly\
  prohibited at the park.", price="$25.00", category= category2)

session.add(Item5)
session.commit()

Item6 = Item(user_id=User3.id, name="Orange Jumpsuit",\
	description="Subsidized by the government for hikers that get lost. \
	All sizes available. Visible up to 7 miles. \
	We are legally required to sell this.", price="$19.99", category= category2)

session.add(Item6)
session.commit()