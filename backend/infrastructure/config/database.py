import os
import json
from sqlalchemy import create_engine, text

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not set. Configure it in your environment variables."
    )

MOCK_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "mock_data.json")

engine = create_engine(DATABASE_URL, future=True, pool_pre_ping=True)


def get_engine():
    return engine


def load_mock_data() -> dict:
    with open(MOCK_DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def init_db():
    from infrastructure.persistence.schema import create_schema, migrate_schema
    from infrastructure.seeders.seeder import seed_data

    with engine.begin() as conn:
        create_schema(conn)
        migrate_schema(conn)
        result = conn.execute(text("SELECT COUNT(*) as cnt FROM users"))
        row = result.mappings().first()
        if row and row["cnt"] == 0:
            data = load_mock_data()
            seed_data(conn, data)
            print("[db] Database seeded with initial data.")
        else:
            print("[db] Database already contains data. Skipping seed.")
    print("[db] Database initialized successfully.")
    return engine
