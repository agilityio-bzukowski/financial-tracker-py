from app.db.schema import Transaction
from app.models.transaction import TransactionCreate, TransactionUpdate
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session


class TransactionService:
    def __init__(self, session: Session):
        self.session = session

    def get_all_transactions(self) -> list[Transaction]:
        result = self.session.execute(select(Transaction))
        return list(result.scalars().all())

    def create_transaction(self, data: TransactionCreate) -> Transaction:
        transaction = Transaction(
            amount=data.amount,
            description=data.description,
            type=data.type.value,
            category_id=data.category_id,
        )
        self.session.add(transaction)
        self.session.commit()
        self.session.refresh(transaction)
        return transaction

    def get_transaction(self, transaction_id: int) -> Transaction | None:
        return self.session.get(Transaction, transaction_id)

    def update_transaction(
        self, transaction_id: int, data: TransactionUpdate
    ) -> Transaction:
        db_transaction = self.get_transaction(transaction_id)
        if not db_transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        update = data.model_dump(exclude_unset=True)
        for key, value in update.items():
            if key == "type":
                setattr(db_transaction, key, value.value if hasattr(value, "value") else value)
            else:
                setattr(db_transaction, key, value)
        self.session.commit()
        self.session.refresh(db_transaction)
        return db_transaction

    def delete_transaction(self, transaction_id: int) -> bool:
        transaction = self.get_transaction(transaction_id)
        if transaction:
            self.session.delete(transaction)
            self.session.commit()
            return True
        return False
