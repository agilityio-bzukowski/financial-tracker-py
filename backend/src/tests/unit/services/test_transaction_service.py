"""Unit tests for TransactionService."""

import pytest
from app.models.transaction import TransactionCreate, TransactionType, TransactionUpdate
from app.services.transaction_service import TransactionService
from tests.factories import TransactionCategoryFactory, TransactionFactory


@pytest.mark.unit
class TestTransactionService:
    """Test suite for TransactionService."""

    def test_get_all_transactions(self, session):
        """Test getting all transactions."""
        TransactionFactory.create_batch(5)
        service = TransactionService(session)
        result = service.get_all_transactions(page=1, limit=10)
        assert result.total == 5
        assert len(result.items) == 5
        assert result.page == 1
        assert result.limit == 10

    def test_create_transaction(self, session):
        """Test creating a transaction."""
        category = TransactionCategoryFactory()
        service = TransactionService(session)
        create_dto = TransactionCreate(
            amount=100.50,
            description="Test income",
            type=TransactionType.INCOME,
            category_id=category.id,
        )
        result = service.create_transaction(create_dto)
        assert result.id is not None
        assert result.amount == create_dto.amount
        assert result.description == create_dto.description
        assert result.type == create_dto.type.value
        assert result.category_id == create_dto.category_id

    def test_get_transaction(self, session):
        transaction = TransactionFactory()
        """Test getting a transaction by id."""
        service = TransactionService(session)
        result = service.get_transaction(transaction.id)
        assert result is not None
        assert result.id == transaction.id
        assert result.amount == transaction.amount
        assert result.description == transaction.description
        assert result.type == transaction.type
        assert result.category_id == transaction.category_id

    def test_update_transaction(self, session):
        transaction = TransactionFactory()
        """Test updating a transaction."""
        service = TransactionService(session)
        update_dto = TransactionUpdate(
            amount=999.99,
            description="Updated description",
            type=(
                TransactionType(transaction.type)
                if isinstance(transaction.type, str)
                else transaction.type
            ),
            category_id=transaction.category_id,
        )
        result = service.update_transaction(transaction.id, update_dto)
        assert result.id == transaction.id
        assert result.amount == update_dto.amount
        assert result.description == update_dto.description
        assert result.type == update_dto.type.value
        assert result.category_id == update_dto.category_id

    def test_delete_transaction(self, session):
        transaction = TransactionFactory()
        """Test deleting a transaction."""
        service = TransactionService(session)
        tid = transaction.id
        result = service.delete_transaction(tid)
        assert result is True
        assert service.get_transaction(tid) is None
