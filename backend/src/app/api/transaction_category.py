from app.db.schema import get_session
from app.models.transaction_category import TransactionCategoryRead
from app.services.transaction_category_service import TransactionCategoryService
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter(prefix="/transaction_categories", tags=["transaction_categories"])


@router.get("/", response_model=list[TransactionCategoryRead])
def list_transaction_categories(session: Session = Depends(get_session)):
    service = TransactionCategoryService(session)
    transaction_categories = service.get_all_transaction_categories()
    return [TransactionCategoryRead.model_validate(t) for t in transaction_categories]
