"""Modelos declarativos SQLAlchemy 2.0 para seguimiento de proyectos de datos."""

from sqlalchemy import Boolean, CheckConstraint, Float, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Registro común de metadatos para los modelos ORM."""


class Dataset(Base):
    """Información básica sobre una fuente de datos utilizada en un proyecto."""

    __tablename__ = "datasets"
    __table_args__ = (
        CheckConstraint("num_rows >= 0", name="ck_datasets_num_rows_no_negativo"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    source_url: Mapped[str] = mapped_column(String(500), nullable=False)
    num_rows: Mapped[int] = mapped_column(Integer, nullable=False)

    def __repr__(self) -> str:
        return f"Dataset(id={self.id!r}, name={self.name!r}, num_rows={self.num_rows!r})"


class ModelExperiment(Base):
    """Experimento de Machine Learning y resultado de precisión obtenido."""

    __tablename__ = "model_experiments"
    __table_args__ = (
        CheckConstraint("accuracy >= 0 AND accuracy <= 1", name="ck_model_experiments_accuracy"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    algorithm_name: Mapped[str] = mapped_column(String(120), nullable=False)
    accuracy: Mapped[float] = mapped_column(Float, nullable=False)
    is_deployed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    def __repr__(self) -> str:
        return (
            f"ModelExperiment(id={self.id!r}, algorithm_name={self.algorithm_name!r}, "
            f"accuracy={self.accuracy!r}, is_deployed={self.is_deployed!r})"
        )
