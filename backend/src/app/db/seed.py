"""
Seed script for transaction categories.

Run with: python -m app.db.seed
Or from backend directory: poetry run python -m app.db.seed
"""

from app.db.schema import SessionLocal, TransactionCategory


def seed_transaction_categories() -> None:
    """Insert default transaction categories if they don't exist."""
    categories = [
        {"name": "Food & Dining", "description": "Food and dining expenses, etc."},
        {"name": "Transportation", "description": "Bus, train, taxi, fuel, etc."},
        {"name": "Shopping", "description": "Shopping expenses, etc."},
        {"name": "Entertainment", "description": "Movies, concerts, etc."},
        {"name": "Bills & Utilities", "description": "Electricity, water, internet, etc."},
        {"name": "Income", "description": "Income from salary, investments, etc."},
        {"name": "Transfer", "description": "Transfer between accounts, etc."},
    ]

    with SessionLocal() as session:
        for cat_data in categories:
            existing = (
                session.query(TransactionCategory)
                .filter_by(name=cat_data["name"])
                .first()
            )
            if not existing:
                session.add(TransactionCategory(**cat_data))
        session.commit()
        print(f"Seeded {len(categories)} transaction categories.")


if __name__ == "__main__":
    seed_transaction_categories()
