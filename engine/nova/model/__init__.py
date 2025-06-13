from .hot_rec import (
    get_hot_by_uid,
    get_new_by_uid,
    insert_uid_history,
    start_cache_update_thread,
)
from .hot_search import get_hot_by_keyword
from .op_mysql import delete, insert, query_by_page, select, select_by_set_codes, update
from .toy_brands import TABLE_NAME as TOY_BRANDS_TABLE_NAME
from .toy_brands import create_toy_brands_table
from .toy_kit import TABLE_NAME as TOY_KIT_TABLE_NAME
from .toy_kit import create_toy_kit_table, insert_kit_table
from .toy_themes import TABLE_NAME as TOY_THEMES_TABLE_NAME
from .toy_themes import create_toy_themes_table

create_toy_brands_table()
create_toy_kit_table()
# insert_kit_table()
create_toy_themes_table()
start_cache_update_thread()

__all__ = [
    "delete",
    "insert",
    "query_by_page",
    "select",
    "update",
    "TOY_BRANDS_TABLE_NAME",
    "TOY_KIT_TABLE_NAME",
    "TOY_THEMES_TABLE_NAME",
    "get_hot_by_uid",
    "get_new_by_uid",
    "select_by_set_codes",
    "insert_uid_history",
    "get_hot_by_keyword",
]
