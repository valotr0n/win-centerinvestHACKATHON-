from logging.config import fileConfig
import sys
from os.path import abspath, dirname

from sqlalchemy import engine_from_config, create_engine
from sqlalchemy import pool
from alembic import context

sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))

from app.config import settings
from app.database import Base
from app.users.models import Users, Role

# Alembic Config
config = context.config

# Используйте синхронный URL для Alembic
config.set_main_option("sqlalchemy.url", settings.SYNC_DATABASE_URL)

# Создайте синхронный движок
def run_migrations_offline():
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=Base.metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

def run_migrations_online():
    connectable = create_engine(config.get_main_option("sqlalchemy.url"))

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=Base.metadata,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
