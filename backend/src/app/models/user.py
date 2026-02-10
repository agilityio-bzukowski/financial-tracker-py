import pydantic


class UserBase(pydantic.BaseModel):
    email: str
    hashed_password: str


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    is_active: bool
