from app.db.schema import TransactionCategory
from app.models.transaction_category import TransactionCategoryCreate
from sqlalchemy import select
from sqlalchemy.orm import Session


class TransactionCategoryService:
    def __init__(self, session: Session):
        self.session = session

    def get_all_transaction_categories(self) -> list[TransactionCategory]:
        result = self.session.execute(select(TransactionCategory))
        return list[TransactionCategory](result.scalars().all())

    def get_transaction_category(
        self, transaction_category_id: int
    ) -> TransactionCategory | None:
        return self.session.get(TransactionCategory, transaction_category_id)

    def create_transaction_category(
        self, data: TransactionCategoryCreate
    ) -> TransactionCategory:
        transaction_category = TransactionCategory(
            name=data.name, description=data.description
        )
        self.session.add(transaction_category)
        self.session.commit()
        self.session.refresh(transaction_category)
        return transaction_category
