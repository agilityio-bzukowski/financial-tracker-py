"""Factory-boy factories for generating test data."""
import factory
from app.db.schema import Transaction, TransactionCategory
from app.models.transaction import TransactionType


class TransactionCategoryFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory for creating TransactionCategory test instances."""
    
    class Meta:
        model = TransactionCategory
        sqlalchemy_session_persistence = "commit"
    
    name = factory.Sequence(lambda n: f"Category {n}")
    description = factory.Faker("sentence", nb_words=5)


class TransactionFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory for creating Transaction test instances."""
    
    class Meta:
        model = Transaction
        sqlalchemy_session_persistence = "commit"
    
    amount = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True)
    description = factory.Faker("sentence", nb_words=6)
    type = factory.Iterator([TransactionType.INCOME, TransactionType.EXPENSE])
    category = factory.SubFactory(TransactionCategoryFactory)
