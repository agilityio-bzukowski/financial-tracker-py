from enum import Enum

from pydantic import BaseModel, ConfigDict


class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"


class TransactionBase(BaseModel):
    amount: float
    description: str
    type: TransactionType
    category_id: int


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(TransactionBase):
    pass


class TransactionRead(TransactionBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
