from app.api import transactions
from app.core.config import config
from fastapi import FastAPI

app = FastAPI(title=config.app_name)


# Register routes
app.include_router(transactions.router)
