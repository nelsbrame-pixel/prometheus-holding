from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://prometheus_5ipv_user:Ieq8J1YeUMVbDYdEcI1zYCTohfHdVdx5@dpg-d7nrnkrbc2fs7391avq0-a.oregon-postgres.render.com/prometheus_5ipv"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()