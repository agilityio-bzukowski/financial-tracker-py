from app.db.schema import get_session
from app.models.transaction import TransactionCreate, TransactionRead, TransactionUpdate
from app.services.transaction_service import TransactionService
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get("/", response_model=list[TransactionRead])
def list_transactions(session: Session = Depends(get_session)):
    service = TransactionService(session)
    transactions = service.get_all_transactions()
    return [TransactionRead.model_validate(t) for t in transactions]


@router.get("/{transaction_id}", response_model=TransactionRead)
def get_transaction(
    transaction_id: int,
    session: Session = Depends(get_session),
):
    service = TransactionService(session)
    transaction = service.get_transaction(transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return TransactionRead.model_validate(transaction)


@router.post("/", response_model=TransactionRead)
def create_transaction(
    data: TransactionCreate,
    session: Session = Depends(get_session),
):
    service = TransactionService(session)
    transaction = service.create_transaction(data)
    return TransactionRead.model_validate(transaction)


@router.put("/{transaction_id}", response_model=TransactionRead)
def update_transaction(
    transaction_id: int,
    data: TransactionUpdate,
    session: Session = Depends(get_session),
):
    service = TransactionService(session)
    transaction = service.update_transaction(transaction_id, data)
    return TransactionRead.model_validate(transaction)


@router.delete("/{transaction_id}", status_code=204)
def delete_transaction(
    transaction_id: int,
    session: Session = Depends(get_session),
):
    service = TransactionService(session)
    if not service.delete_transaction(transaction_id):
        raise HTTPException(status_code=404, detail="Transaction not found")
