from sqlmodel import create_engine, SQLModel, Session
from config.settings import DATABASE_URL

class DataBase:
    engine = create_engine(DATABASE_URL, echo=False)
        
    def init_db():
        SQLModel.metadata.create_all(DataBase.engine)
    
    def get_session():
        with Session(DataBase.engine) as session:
            yield session