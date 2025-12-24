
from sqlalchemy import create_engine, inspect
from dotenv import load_dotenv
import os

load_dotenv()

# FORCE SQLITE for verification
os.environ["CULTIVAR_DB_DRIVER"] = "sqlite"
if not os.getenv("SQLITE_DB_PATH"):
    os.environ["SQLITE_DB_PATH"] = "instance/cultivar.db"

from app.config.config import Config

db_url = Config.get_database_uri()
# Handle async url if present
if "sqlite+aiosqlite" in db_url:
    db_url = db_url.replace("sqlite+aiosqlite", "sqlite")

engine = create_engine(db_url)
inspector = inspect(engine)
tables = inspector.get_table_names()
print(f"Existing Tables: {tables}")
print(f"Total Tables: {len(tables)}")
