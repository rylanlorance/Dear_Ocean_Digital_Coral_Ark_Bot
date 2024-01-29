from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, DateTime, Integer, Date
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class Donor(Base):
    __tablename__ = "donor"
    
    donor_id: Mapped[str] = mapped_column(String, primary_key=True)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)


    __table_args__= {'schema': 'dca'}