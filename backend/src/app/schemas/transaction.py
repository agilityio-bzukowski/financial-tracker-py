from pydantic import BaseModel, ConfigDict


class TransactionBase(BaseModel):
    amount: float
    description: str


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    amount: float | None = None
    description: str | None = None


class TransactionRead(TransactionBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
