"""mykeibadb-python: JRA競馬データベースへのPythonアクセスライブラリ

このライブラリは、mykeibadbで構築されたPostgreSQLデータベースから
競馬データを取得するための統一的なインターフェースを提供します。
"""

try:
    from importlib.metadata import PackageNotFoundError, version

    __version__ = version("mykeibadb-python")
except (PackageNotFoundError, ImportError):
    __version__ = "unknown"

from mykeibadb.config import ConfigManager
from mykeibadb.connection import ConnectionManager
from mykeibadb.exceptions import (
    InvalidFilterError,
    MykeibaDBError,
    TableNotFoundError,
    ValidationError,
)
from mykeibadb.getters import (
    BaseGetter,
    ChokyoGetter,
    HyosuGetter,
    KyosobaGetter,
    MasterGetter,
    MiningGetter,
    OddsGetter,
    OthersGetter,
    RaceGetter,
    ShussobetsuGetter,
    SokuhoGetter,
    Win5Getter,
)
from mykeibadb.tables import TableAccessor
from mykeibadb.utils import (
    is_valid_identifier,
    validate_banushi_code,
    validate_chokyoshi_code,
    validate_hanshoku_toroku_bango,
    validate_kaisai_code,
    validate_keibajo_code,
    validate_ketto_toroku_bango,
    validate_kishu_code,
    validate_race_code,
    validate_seisansha_code,
    validate_tracen_kubun,
    validate_track_code,
)

__all__ = [
    "__version__",
    "ConfigManager",
    "ConnectionManager",
    "MykeibaDBError",
    "TableNotFoundError",
    "InvalidFilterError",
    "ValidationError",
    "TableAccessor",
    # Getter classes
    "BaseGetter",
    "RaceGetter",
    "HyosuGetter",
    "OddsGetter",
    "MasterGetter",
    "ShussobetsuGetter",
    "ChokyoGetter",
    "KyosobaGetter",
    "MiningGetter",
    "Win5Getter",
    "SokuhoGetter",
    "OthersGetter",
    # Validators
    "is_valid_identifier",
    "validate_race_code",
    "validate_ketto_toroku_bango",
    "validate_kishu_code",
    "validate_chokyoshi_code",
    "validate_seisansha_code",
    "validate_banushi_code",
    "validate_kaisai_code",
    "validate_hanshoku_toroku_bango",
    "validate_keibajo_code",
    "validate_track_code",
    "validate_tracen_kubun",
]
