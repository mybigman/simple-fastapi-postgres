from alembic import context
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool

from app.core.config import settings


# Alembic Config object provides access to the values in the .ini file.
config = context.config
config.set_main_option("sqlalchemy.url", settings.SQLALCHEMY_DATABASE_URL)  # type: ignore


# Setup loggers according to the configuration in the .ini file.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Add 'autogenerate' support, target the metadata of the base models class.
from app.db.alembic import Base

target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),  # type: ignore
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
