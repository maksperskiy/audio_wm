from sqlalchemy import Column, DateTime, Numeric, Integer, String, func

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ParamsModel(Base):
    __tablename__ = "params_history"

    step_number = Column(Integer, primary_key=True)
    label = Column(String(255), primary_key=True)

    param_number = Column(Integer)

    freq_bottom = Column(Numeric, nullable=False)
    freq_top = Column(Numeric, nullable=False)
    duration = Column(Numeric, nullable=False)
    freq_bottom_grad = Column(Numeric)
    freq_top_grad = Column(Numeric)
    duration_grad = Column(Numeric)
    freq_bottom_step = Column(Numeric, nullable=False)
    freq_top_step = Column(Numeric, nullable=False)
    duration_step = Column(Numeric, nullable=False)

    expert_score = Column(Numeric)
    sound_noise_ratio = Column(Numeric)
    success_ratio = Column(Numeric)

    created_at = Column(DateTime, server_default=func.now())
