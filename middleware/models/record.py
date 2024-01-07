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

class Record(Base):
    __tablename__ = "record"

    record_id: Mapped[int] = mapped_column(primary_key=True)
    location_id: Mapped[str] = mapped_column(String(50))
    #description
    recorded_dt: Mapped[datetime] = mapped_column(Date)
    uploaded_dt: Mapped[datetime] = mapped_column(Date)
    species_tag_1: Mapped[str] = mapped_column(String)
    species_tag_2: Mapped[str] = mapped_column(String)
    google_drive_url: Mapped[str] = mapped_column(String)
    filename_string: Mapped[str] = mapped_column(String)
    file_extension: Mapped[str] = mapped_column(String)
    image_id: Mapped[str] = mapped_column(String)
    tagger_id: Mapped[int] = mapped_column(Integer)
    donor_id: Mapped[str] = mapped_column(String)

    __table_args__= {'schema': 'dca'}