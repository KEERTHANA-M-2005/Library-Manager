from sqlalchemy import create_engine

DATABASE_URL = "mysql+pymysql://root:@localhost:3306/library_db"

engine = create_engine(DATABASE_URL)
