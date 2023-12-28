from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, DateTime, Integer, Date
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from datetime import datetime

class Base(DeclarativeBase):
    pass

class Species(Base):
    __tablename__ = "species"

    species_id: Mapped[str] = mapped_column(String(7), primary_key=True)
    family: Mapped[str] = mapped_column(String)
    species: Mapped[str] = mapped_column(String)
    species_common_name: Mapped[str] = mapped_column(String)

    __table_args__ = {'schema': 'species_codebook'}
