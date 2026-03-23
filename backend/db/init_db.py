from backend.db.base import Base
from backend.db.session import engine
import backend.models.scan_record  # noqa: F401


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
