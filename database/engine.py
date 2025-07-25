from sqlmodel import create_engine

engine = create_engine("sqlite:///./database/database.db", echo=True)