from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# palitan mo yung password kung iba sa 'root'
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:12345@localhost/pricing_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
