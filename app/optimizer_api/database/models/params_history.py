from sqlalchemy import BIGINT, Column, DateTime, Integer, Numeric, String, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ParamsHistoryModel(Base):
    __tablename__ = "params_history"

    step_number = Column(Integer, primary_key=True)
    experiment_number = Column(Integer, primary_key=True)
    label = Column(String(255), primary_key=True)

    current_param = Column(Integer)
    batch_size = Column(Integer, default=1)

    message = Column(BIGINT)

    param_number = Column(Integer)

    freq_bottom = Column(Integer, nullable=False)
    freq_top = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)
    freq_bottom_grad = Column(Numeric)
    freq_top_grad = Column(Numeric)
    duration_grad = Column(Numeric)
    freq_bottom_step = Column(Integer, nullable=False)
    freq_top_step = Column(Integer, nullable=False)
    duration_step = Column(Integer, nullable=False)

    expert_score = Column(Numeric)
    sound_noise_ratio = Column(Numeric)
    success_ratio = Column(Numeric)

    created_at = Column(DateTime, server_default=func.now())
