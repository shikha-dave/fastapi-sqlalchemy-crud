# FastAPI CRUD Application with SQLAlchemy

A REST API built using **FastAPI, SQLAlchemy 2.0, and SQLite** to manage items and categories. This project demonstrates CRUD operations, relational database handling, ORM relationships, and Pydantic response validation.

## Features

- Create, retrieve, update, and delete items.
- Create, retrieve, update, and delete categories.
- One-to-many relationship between Categories and Items.
- SQLAlchemy ORM using `Mapped`, `mapped_column`, and `relationship`.
- Foreign key constraints between database tables.
- Nullable category relationships.
- Pydantic schemas for request validation and response serialization.
- Nested and flattened relationship data using `AliasPath`.
- HTTP exception handling for missing records.
- Eager loading using `selectinload()` and `joinedload()`.

## Tech Stack

- Python
- FastAPI
- SQLAlchemy 2.0
- Pydantic
- SQLite
- Uvicorn

## Project Structure

```text
fastapi-sqlalchemy-crud/
│
├── main.py
├── models.py
├── schemas.py
├── database.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Database Relationship

The application implements a one-to-many relationship:

- One Category can have multiple Items.
- Each Item can belong to one Category.
- An Item can also exist without a Category.

```text
Category (1) ─────────── (*) Item
```

The `items` table contains a nullable `category_id` foreign key referencing `categories.id`.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/shikha-dave/fastapi-sqlalchemy-crud.git
cd fastapi-sqlalchemy-crud
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
uvicorn main:app --reload
```

The API will be available at:

`http://127.0.0.1:8000`

### 6. Access API documentation

FastAPI provides interactive Swagger documentation:

`http://127.0.0.1:8000/docs`

## API Endpoints

### Items

| Method | Endpoint | Description |
|---|---|---|
| POST | `/items` | Create an item |
| GET | `/items` | Retrieve all items |
| GET | `/items/joined` | Retrieve all items using joinedload |
| GET | `/items/eager` | Retrieve all items using selectinload |
| GET | `/items/{item_id}` | Retrieve a specific item |
| PUT | `/items/{item_id}` | Update an item |
| PATCH | `/items/{item_id}` | Partially update an item |
| DELETE | `/items/{item_id}` | Delete an item |
| DELETE | `/items` | Delete all items |

### Categories

| Method | Endpoint | Description |
|---|---|---|
| POST | `/category` | Create a category |
| GET | `/categories` | Retrieve all categories |
| GET | `/categories/{category_id}` | Retrieve a specific category |
| PUT | `/category/{category_id}` | Update a category |
| DELETE | `/category/{category_id}` | Delete a category |
| DELETE | `/categories` | Delete all categories |

## Example Item Response

[
  {
    "id": 0,
    "name": "string",
    "description": "string",
    "price": 0,
    "quantity": 0,
    "category_id": 0,
    "category_name": "string"
  }
]