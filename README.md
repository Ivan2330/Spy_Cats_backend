---

# Spy Cat Agency — Backend (FastAPI)
<img width="1807" height="891" alt="image" src="https://github.com/user-attachments/assets/ab1631be-41a7-4f32-b0e4-f4c9f10507b0" />

## Overview

This backend implements the **Spy Cat Agency assessment**. It provides a REST API with validation, asynchronous PostgreSQL access, migrations with Alembic, and breed validation via **TheCatAPI**.

Features include **CRUD for Spy Cats**, **missions and targets management**, and **business rules enforcement** (immutability of notes, one mission per cat, etc.).

**Stack:** FastAPI · Pydantic v2 · SQLAlchemy (async) · Alembic · PostgreSQL · Uvicorn · httpx

---

## Features

### Spy Cats

* Create a cat with `name`, `years_experience`, `breed`, `salary`
* Breed validated via TheCatAPI
* Update salary
* List cats, get single cat
* Delete cat

### Missions & Targets

* Create a mission with 1–3 targets in a single request
* Assign mission to a cat (only one active mission per cat)
* Update target fields (`name`, `country`, `notes`, `complete`)
* Notes cannot be updated if the mission or target is complete
* Auto-complete missions when all targets are marked complete
* List missions and retrieve single mission

### Validation & Error Handling

* Pydantic request validation
* Consistent error responses (`422`, `409`, `404`)

---

## Project Structure

```
backend/
├─ alembic/
│  ├─ versions/              <- migration scripts
│  └─ env.py
├─ app/
│  ├─ __pycache__/
│  ├─ core/
│  │  ├─ __pycache__/
│  │  ├─ __init__.py
│  │  ├─ config.py
│  │  ├─ errors.py
│  │  └─ logging.py
│  ├─ database/
│  │  ├─ __init__.py
│  │  └─ db.py
│  ├─ models/
│  │  ├─ __init__.py
│  │  ├─ cat.py
│  │  ├─ mission.py
│  │  └─ target.py
│  ├─ routers/
│  │  ├─ __init__.py
│  │  ├─ cat_router.py
│  │  ├─ mission_router.py
│  │  └─ health_router.py
│  ├─ schemas/
│  │  ├─ __init__.py
│  │  ├─ cat.py
│  │  ├─ mission.py
│  │  └─ target.py
│  ├─ services/
│  │  ├─ __init__.py
│  │  └─ cat_breeds.py
│  ├─ __init__.py
│  └─ main.py
├─ postman/                  <- Postman collection goes here
├─ venv/                     <- virtual environment (ignored in VCS)
├─ .env
├─ .env.example
├─ alembic.ini
├─ README.md
└─ requirements.txt
```

---

## Environment Variables

Create a `.env` file from `.env.example`:

```bash
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/spycat
THECATAPI_BASE=https://api.thecatapi.com/v1/breeds
THECATAPI_KEY=         # optional
CORS_ORIGINS=http://localhost:3000
```

---

## Setup & Run

### 1. Create virtual environment and install dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run database migrations

```bash
alembic upgrade head
```

### 3. Start the server

```bash
uvicorn app.main:app --reload
```

API available at: [http://127.0.0.1:8000](http://127.0.0.1:8000)
Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
Healthcheck: `GET /health` → `{"status":"ok"}`

---

## Postman Collection

- View on GitHub:  
  [SpyCatAgency.postman_collection.json](backend/postman/SpyCatAgency.postman_collection.json)

- Import directly into Postman (raw link):  
  [Download Collection (raw)](https://raw.githubusercontent.com/Ivan2330/Spy_Cats_backend/main/backend/postman/SpyCatAgency.postman_collection.json)

---

## Data Models

**Cat**

* `id: int`
* `name: str`
* `years_experience: int`
* `breed: str` (validated)
* `salary: float`

**Mission**

* `id: int`
* `cat_id: int | null`
* `complete: bool`
* `targets: List[Target]`

**Target**

* `id: int`
* `mission_id: int`
* `name: str`
* `country: str`
* `notes: str`
* `complete: bool`

---

## Business Rules

1. Breed must exist in TheCatAPI
2. Only one active mission per cat
3. Mission must include 1–3 targets
4. Notes cannot be updated if mission/target is complete
5. Mission auto-completes when all targets are complete

---

## REST API Endpoints

### Cats

* **POST /cats** → create a cat
* **GET /cats** → list cats
* **GET /cats/{id}** → get a cat
* **PATCH /cats/{id}/salary** → update salary
* **DELETE /cats/{id}** → delete a cat

### Missions

* **POST /missions** → create mission with targets
* **GET /missions** → list missions
* **GET /missions/{id}** → get mission by ID
* **PATCH /missions/{id}/assign** → assign mission to a cat
* **PATCH /missions/{id}/targets/{target_id}** → update target (fields, notes, complete rules enforced)

---

## cURL Examples

**Create a cat**

```bash
curl -X POST http://localhost:8000/cats \
 -H "Content-Type: application/json" \
 -d '{"name":"Whisker Black","years_experience":4,"breed":"Sphynx","salary":3200}'
```

**Create a mission**

```bash
curl -X POST http://localhost:8000/missions \
 -H "Content-Type: application/json" \
 -d '{"targets":[
       {"name":"Mr. Johnson","country":"France","notes":"Observed entering embassy"},
       {"name":"Agent X","country":"Germany","notes":"Frequent cafe visits"}
     ]}'
```

**Assign mission**

```bash
curl -X PATCH http://localhost:8000/missions/1/assign \
 -H "Content-Type: application/json" \
 -d '{"cat_id":1}'
```

**Update target notes**

```bash
curl -X PATCH http://localhost:8000/missions/1/targets/2 \
 -H "Content-Type: application/json" \
 -d '{"notes":"Switched disguise","complete":true}'
```

---

## Postman Collection

The collection is provided under:
`postman/SpyCatAgency.postman_collection.json`

Includes requests for:

* Cats CRUD
* Mission creation/assignment
* Target updates


---

## Frontend

A separate Next.js repository implements the Spy Cat Dashboard:

* List cats
* Create a new cat
* Update cat salary
* Delete cat

---
