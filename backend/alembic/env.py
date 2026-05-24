from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from core.database.base import Base

# =====================================================
# ALEMBIC CONFIG
# =====================================================

config = context.config

# =====================================================
# LOGGING
# =====================================================

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# =====================================================
# METADATA
# =====================================================

target_metadata = Base.metadata

# =====================================================
# IGNORE POSTGIS INTERNAL TABLES
# =====================================================


def include_object(
    object,
    name,
    type_,
    reflected,
    compare_to,
):

    ignored_tables = {
        # postgis
        "spatial_ref_sys",
        "geometry_columns",
        "geography_columns",
        # tiger geocoder
        "addr",
        "addrfeat",
        "bg",
        "county",
        "county_lookup",
        "countysub_lookup",
        "cousub",
        "direction_lookup",
        "edges",
        "faces",
        "featnames",
        "geocode_settings",
        "geocode_settings_default",
        "layer",
        "loader_lookuptables",
        "loader_platform",
        "loader_variables",
        "pagc_gaz",
        "pagc_lex",
        "pagc_rules",
        "place",
        "place_lookup",
        "secondary_unit_lookup",
        "state",
        "state_lookup",
        "street_type_lookup",
        "tabblock",
        "tabblock20",
        "topology",
        "tract",
        "zcta5",
        "zip_lookup",
        "zip_lookup_all",
        "zip_lookup_base",
        "zip_state",
        "zip_state_loc",
    }

    if type_ == "table" and name in ignored_tables:

        return False

    return True


# =====================================================
# OFFLINE MIGRATIONS
# =====================================================


def run_migrations_offline() -> None:

    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():

        context.run_migrations()


# =====================================================
# ONLINE MIGRATIONS
# =====================================================


def run_migrations_online() -> None:

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            include_schemas=False,
            include_object=include_object,
        )

        with context.begin_transaction():

            context.run_migrations()


# =====================================================
# EXECUTION
# =====================================================

if context.is_offline_mode():

    run_migrations_offline()

else:

    run_migrations_online()
