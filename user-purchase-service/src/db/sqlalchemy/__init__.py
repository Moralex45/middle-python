import asyncio

from src.db.sqlalchemy.core import init_models

if __name__ == '__main__':
    asyncio.run(init_models())
