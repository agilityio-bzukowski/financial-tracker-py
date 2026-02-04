from fastapi import APIRouter

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get("/hello")
def hello():
    return {"message": "Hello from transactions!"}
