from app.core.config import config
from sqlalchemy import ForeignKey, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,
)
from sqlalchemy.orm.session import Session

engine = create_engine(config.db_url)
SessionLocal = sessionmaker[Session](autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_session():
    with SessionLocal() as session:
        yield session


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[float]
    description: Mapped[str]
    type: Mapped[str]
    category_id: Mapped[int] = mapped_column(ForeignKey("transaction_categories.id"))

    category: Mapped["TransactionCategory"] = relationship(
        "TransactionCategory", back_populates="transactions"
    )


class TransactionCategory(Base):
    __tablename__ = "transaction_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str | None]

    transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction", back_populates="category"
    )


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
