from fastapi import FastAPI, Depends

from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session, selectinload, joinedload
from sqlalchemy import select
import models
from database import Base, engine, get_db
from fastapi import HTTPException
from schemas import CategoryCreate, CategoryResponse, ItemCreate, ItemResponse, ItemUpdate, CategoryUpdate


Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Welcome to the SQLLITE and SQLALCHEMY!"}

@app.get("/items", response_model=list[ItemResponse])
def get_items(db: Session = Depends(get_db)):
    items = db.query(models.Item).all()
    return items

@app.get("/items/joined", response_model=list[ItemResponse])
def get_items_joined(db: Session = Depends(get_db)):
    items = db.query(models.Item).options(joinedload(models.Item.category)).all()
    return items

@app.get("/items/eager", response_model=list[ItemResponse])
def get_items_eager(db: Session = Depends(get_db)):
    items = db.query(models.Item).options(selectinload(models.Item.category)).all()
    return items 

@app.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Session= Depends(get_db)):
    db_item = db.get(models.Item, item_id)
    if not db_item:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    return db_item




@app.post("/items", response_model=ItemResponse)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = models.Item(
        name=item.name,
        description=item.description,
        price=item.price, 
        category_id=item.category_id,
        quantity=item.quantity

    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@app.put("/items/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, updated_item: ItemUpdate, db: Session = Depends(get_db)):
    db_item = db.get(models.Item, item_id)
    if not db_item:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )
    for key, value in updated_item.model_dump(exclude_unset=True).items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

# delete single item
@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.get(models.Item, item_id)
    if not db_item:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )
    db.delete(db_item)
    db.commit()
    return {"message": "Item deleted successfully"}


# function to patch

@app.patch("/items/{item_id}", response_model=ItemResponse)
def patch_item(item_id: int, updated_item: ItemUpdate, db: Session = Depends    (get_db)):
    db_item = db.get(models.Item, item_id)
    if not db_item:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )
    for key, value in updated_item.model_dump(exclude_unset=True).items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item


@app.delete("/items/{item_id}")
def delete_all_items(db: Session = Depends(get_db)):
    db.query(models.Item).delete()
    db.commit()
    return {"message": "All Items deleted successfully"}


@app.get("/categories", response_model=list[CategoryResponse])
def get_all_Categories(db: Session = Depends(get_db)):
    categories = db.query(models.Category).all()
    return categories

@app.get("/categories/{category_id}")
def get_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.get(models.Category, category_id)
    if not db_category:
        raise HTTPException(
            status_code=404, 
            detail="Category not found!"
        )
    return CategoryResponse(**db_category.__dict__)

@app.post("/category")
def create_category(category:CategoryCreate, db: Session = Depends(get_db)):
    db_category = models.Category(
        name = category.name,
        description = category.description
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@app.put("/category/{category_id}")
def update_category(category_id: int, category: CategoryUpdate, db: Session = Depends(get_db)):
    db_category = db.get(models.Category, category_id)
    if not db_category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )
    if category.name is not None:
        db_category.name = category.name
    if category.description is not None:
        db_category.description = category.description
    db.commit()
    db.refresh(db_category)
    return db_category

@app.delete("/category/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.get(models.Category, category_id)
    if not db_category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )
    db.delete(db_category)
    db.commit()
    return {"message": "Category deleted successfully"}

@app.delete("/categories")
def delete_all_categories(db: Session = Depends(get_db)):
    db.query(models.Category).delete()
    db.commit()
    return {"message": "All Categories deleted successfully"}

@app.delete("/items")
def delete_all_items(db: Session = Depends(get_db)):
    db.query(models.Item).delete()
    db.commit()
    return {"message": "All Items deleted successfully"}

