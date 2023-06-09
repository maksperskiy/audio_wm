from sqlalchemy import BIGINT, Column, DateTime, Integer, Numeric, String, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ParamsModel(Base):
    __tablename__ = "params"

    label = Column(String(255), primary_key=True)

    message = Column(BIGINT)

    freq_bottom = Column(Integer, nullable=False)
    freq_top = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)

    created_at = Column(DateTime, server_default=func.now())
