"""Integration tests for transaction API endpoints."""

import pytest
from tests.factories import TransactionCategoryFactory, TransactionFactory


@pytest.mark.integration
class TestTransactionAPI:
    """Integration tests for /transactions endpoints."""

    def test_list_transactions_empty(self, client):
        """Test GET /transactions returns empty list when no transactions exist."""
        response = client.get("/transactions")

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert data["page"] == 1
        assert data["limit"] == 10
        assert len(data["items"]) == 0

    def test_list_transactions_with_data(self, client):
        """Test GET /transactions returns paginated list of transactions."""
        category = TransactionCategoryFactory()
        TransactionFactory.create_batch(15, category=category)

        response = client.get("/transactions?page=1&limit=10")

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 15
        assert data["page"] == 1
        assert data["limit"] == 10
        assert len(data["items"]) == 10

        # Verify transaction structure
        transaction = data["items"][0]
        assert "id" in transaction
        assert "amount" in transaction
        assert "description" in transaction
        assert "type" in transaction
        assert "category_id" in transaction

    def test_list_transactions_pagination(self, client):
        """Test pagination works correctly."""
        category = TransactionCategoryFactory()
        TransactionFactory.create_batch(25, category=category)

        # First page
        response = client.get("/transactions?page=1&limit=10")
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 10
        assert data["page"] == 1

        # Second page
        response = client.get("/transactions?page=2&limit=10")
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 10
        assert data["page"] == 2

        # Last page
        response = client.get("/transactions?page=3&limit=10")
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 5
        assert data["page"] == 3

    def test_get_transaction_exists(self, client):
        """Test GET /transactions/{id} returns a specific transaction."""
        category = TransactionCategoryFactory()
        transaction = TransactionFactory(
            category=category, amount=150.75, description="Test transaction"
        )

        response = client.get(f"/transactions/{transaction.id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == transaction.id
        assert data["amount"] == 150.75
        assert data["description"] == "Test transaction"
        assert data["category_id"] == category.id

    def test_get_transaction_not_found(self, client):
        """Test GET /transactions/{id} returns 404 for non-existent transaction."""
        response = client.get("/transactions/999")

        assert response.status_code == 404
        assert "Transaction not found" in response.json()["detail"]

    def test_create_transaction_success(self, client):
        """Test POST /transactions creates a new transaction."""
        category = TransactionCategoryFactory()

        payload = {
            "amount": 200.50,
            "description": "New transaction",
            "type": "expense",
            "category_id": category.id,
        }

        response = client.post("/transactions", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert data["amount"] == 200.50
        assert data["description"] == "New transaction"
        assert data["type"] == "expense"
        assert data["category_id"] == category.id
        assert "id" in data

    def test_create_transaction_invalid_category(self, client):
        """Test POST /transactions returns 404 for invalid category."""
        payload = {
            "amount": 100.00,
            "description": "Test",
            "type": "expense",
            "category_id": 999,  # Non-existent category
        }

        response = client.post("/transactions", json=payload)

        assert response.status_code == 404
        assert "Category not found" in response.json()["detail"]

    def test_create_transaction_invalid_data(self, client):
        """Test POST /transactions validates input data."""
        category = TransactionCategoryFactory()

        # Missing required field
        payload = {
            "amount": 100.00,
            "type": "expense",
            "category_id": category.id,
            # Missing "description"
        }

        response = client.post("/transactions", json=payload)

        assert response.status_code == 422  # Validation error

    def test_update_transaction_success(self, client):
        """Test PUT /transactions/{id} updates an existing transaction."""
        category = TransactionCategoryFactory()
        transaction = TransactionFactory(
            category=category, amount=100.00, description="Original"
        )

        payload = {
            "amount": 250.00,
            "description": "Updated",
            "type": "income",
            "category_id": category.id,
        }

        response = client.put(f"/transactions/{transaction.id}", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert data["amount"] == 250.00
        assert data["description"] == "Updated"
        assert data["type"] == "income"

    def test_update_transaction_not_found(self, client):
        """Test PUT /transactions/{id} returns 404 for non-existent transaction."""
        category = TransactionCategoryFactory()

        payload = {
            "amount": 100.00,
            "description": "Test",
            "type": "expense",
            "category_id": category.id,
        }

        response = client.put("/transactions/999", json=payload)

        assert response.status_code == 404
        assert "Transaction not found" in response.json()["detail"]

    def test_delete_transaction_success(self, client):
        """Test DELETE /transactions/{id} deletes a transaction."""
        category = TransactionCategoryFactory()
        transaction = TransactionFactory(category=category)

        response = client.delete(f"/transactions/{transaction.id}")

        assert response.status_code == 204

        # Verify it's deleted
        get_response = client.get(f"/transactions/{transaction.id}")
        assert get_response.status_code == 404

    def test_delete_transaction_not_found(self, client):
        """Test DELETE /transactions/{id} returns 404 for non-existent transaction."""
        response = client.delete("/transactions/999")

        assert response.status_code == 404
        assert "Transaction not found" in response.json()["detail"]
