from pathlib import Path

from .utils import connect_mysql_database, load_yaml_config, set_log

set_log()

# Load configuration
CONF = load_yaml_config(str((Path(__file__).parent.parent / "config.yaml").resolve()))


mysql_client = connect_mysql_database(
    CONF["mysql"]["host"],
    CONF["mysql"]["port"],
    CONF["mysql"]["user"],
    CONF["mysql"]["password"],
    CONF["mysql"]["database"],
)
