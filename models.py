from sqlmodel import SQLModel, Field

# Define the database model
class Item(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    description: str | None = None
    price: float
    tax: float | None = None