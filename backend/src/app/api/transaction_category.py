from app.db.schema import get_session
from app.models.pagination import PaginatedResponse
from app.models.transaction_category import TransactionCategoryRead
from app.services.transaction_category import TransactionCategoryService
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

router = APIRouter(prefix="/transaction-categories", tags=["transaction-categories"])


@router.get("/", response_model=PaginatedResponse[TransactionCategoryRead])
def list_transaction_categories(
    session: Session = Depends(get_session),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
):
    service = TransactionCategoryService(session)
    transaction_categories = service.get_all_transaction_categories(
        page=page, limit=limit
    )
    return PaginatedResponse(
        page=transaction_categories.page,
        limit=transaction_categories.limit,
        total=transaction_categories.total,
        items=[
            TransactionCategoryRead.model_validate(t)
            for t in transaction_categories.items
        ],
    )
