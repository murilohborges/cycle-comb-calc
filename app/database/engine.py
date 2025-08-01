from sqlmodel import create_engine

engine = create_engine("sqlite:///./app/database/database.db", echo=True)