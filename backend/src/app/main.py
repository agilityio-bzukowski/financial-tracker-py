from app.api import transactions, transaction_category
from app.core.config import config
from fastapi import FastAPI

app = FastAPI(title=config.app_name)


# Register routes
app.include_router(transactions.router)
app.include_router(transaction_category.router)