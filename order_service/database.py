from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import dotenv

# Load environment variables from .env file
USER = dotenv.get_key(".env", "USER")
PWD = dotenv.get_key(".env", "PWD")
DATABASE = dotenv.get_key(".env", "DATABASE_NAME")


# Create a database engine and session
SQLALCHEMY_DATABASE_URL = f"postgresql://{USER}:{PWD}@localhost/{DATABASE}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a base class for our models
SESSION_LOCAL = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# It serves as the base class for declarative models that will be created later.
BASE = declarative_base()

# Dependency function to get a database session
def get_db():
    db = SESSION_LOCAL()
    try:
        yield db
    finally:
        db.close()
