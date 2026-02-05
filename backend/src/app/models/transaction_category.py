from pydantic import BaseModel, ConfigDict


class TransactionCategoryBase(BaseModel):
    name: str
    description: str | None = None


class TransactionCategoryCreate(TransactionCategoryBase):
    pass


class TransactionCategoryUpdate(TransactionCategoryBase):
    pass


class TransactionCategoryRead(TransactionCategoryBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
