from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    first_name: str
    last_name: str | None = None
    phone: str | None = None
    hashed_password: str
    is_active: bool = True