from pathlib import Path
from typing import Optional
from enum import Enum

from sqlmodel import Field, SQLModel, create_engine


class OfferStatus(Enum):
    FREE = 'free'
    RESERVED = 'reserved'
    READY = 'ready'
    TERMINATING = 'terminating'


class Offer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    provider_id: str = Field(default=None, unique=True)
    name: str
    card: str
    status: Optional[OfferStatus] = OfferStatus.FREE
    job_id: Optional[int] = None
    port: Optional[int] = None
    password: Optional[str] = None


sqlite_file_name = Path(__file__).parent.joinpath('./database.db').resolve()
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_db_and_tables()
