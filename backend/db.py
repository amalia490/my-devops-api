from dotenv import load_dotenv
from sqlmodel import create_engine
import os

load_dotenv()

DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "parola")
DB_HOST = "db"

DATABASE_URL = f"postgresql://ama123456:{DB_PASSWORD}@{DB_HOST}:5432/postgresBoard"   
engine = create_engine(DATABASE_URL)

