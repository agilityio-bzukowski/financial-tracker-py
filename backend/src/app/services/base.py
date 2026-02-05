from app.models.pagination import Pagination
from sqlalchemy import func, select
from sqlalchemy.orm import Session


class BaseService:
    def __init__(self, session: Session):
        self.session = session

    def paginate(
        self,
        stmt,
        page: int = 1,
        limit: int = 10,
        max_limit: int = 100,
    ) -> Pagination:
        # normalize data - limit should be between 1 and max_limit
        page = max(page, 1)
        limit = max(1, min(limit, max_limit))

        count_query = select(func.count()).select_from(stmt.subquery())

        total = self.session.scalar(count_query)

        offset = (page - 1) * limit

        items = self.session.scalars(stmt.offset(offset).limit(limit)).all() 

        return Pagination(
            page=page,
            limit=limit,
            total=total,
            items=items,
        )
