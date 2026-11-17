from pydantic import BaseModel, ConfigDict

class ItemCreate(BaseModel):
    name: str
    description: str
    price: int
    quantity: int
    category_id: int | None = None

from pydantic import AliasPath, Field

class ItemResponse(BaseModel):
    id: int
    name: str
    description: str
    price: int
    quantity: int
    category_id: int | None = None
    category_name: str | None = Field(
        default=None,
        validation_alias=AliasPath("category", "name")
    )

    model_config = ConfigDict(from_attributes=True)

class ItemUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
    category_id: int | None = None

    model_config = ConfigDict(from_attributes=True)

class CategoryCreate(BaseModel):
    name: str
    description: str

class CategoryUpdate(BaseModel):
    name: str | None = None
    description: str | None = None

class CategoryResponse(BaseModel):
    id: int
    name:str
    description: str

    model_config = ConfigDict(from_attributes=True)