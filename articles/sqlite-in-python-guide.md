## 1. Should the `.db` file live in Git?

| Scenario | Recommended practice | Rationale |
| --- | --- | --- |
| **Prod/CI** | _Never_ commit the live binary file.  
Commit **migrations** (e.g., Alembic scripts) and/or a schema‑only SQL dump (`sqlite3 db.sqlite .dump > schema.sql`). | Binary deltas bloat the repo and are impossible to diff; schema + migrations are deterministic and reviewable. [Stack Overflow](https://stackoverflow.com/questions/17830882/whats-the-correct-way-to-deal-with-databases-in-git) |
| **Examples, templates** | A read‑only starter database _is_ OK to version (e.g., sample data for tutorials). | File rarely changes, so history churn is negligible. |
| **Local dev data** | Add `*.db`, `*.db‑wal`, `*.db‑shm` to `.gitignore`; optionally a `pre‑commit` hook that unstages accidental additions. [Stack Overflow](https://stackoverflow.com/questions/17830882/whats-the-correct-way-to-deal-with-databases-in-git) |  |

In short: treat the database file like a compiled artifact—recreate it from source (migrations + seed scripts) rather than storing it.

* * *

## 2. Choosing an ORM (or no ORM)

| Style | Library (2025 snapshot) | SQLite support | Notes |
| --- | --- | --- | --- |
| **Micro‑ORM / Dapper‑like** | `pydapper` | ✔ | Direct SQL strings mapped to typed results; sync **and** async DB‑API 2.0 drivers. [GitHub](https://github.com/zschumacher/pydapper)[Stack Overflow](https://stackoverflow.com/questions/54726157/is-there-any-dapper-like-micro-orm-for-python?utm_source=chatgpt.com) |
| **Full‑fat ORM** | `SQLAlchemy 2.0` | ✔ | De‑facto standard; imperative (“class User” models) or SQL expression language; vast ecosystem (Alembic, async). |
| **Pydantic + SQLAlchemy hybrid** | `SQLModel` | ✔ | Combines Pydantic validation + SQLAlchemy core; feels like POCOs with attributes; first‑class type hints. [Better Stack](https://betterstack.com/community/guides/scaling-python/sqlmodel-orm/?utm_source=chatgpt.com) |
| **Lightweight ORM** | `Peewee` | ✔ | Small API surface, great for embedded apps. [docs.peewee-orm.com](https://docs.peewee-orm.com/en/latest/?utm_source=chatgpt.com) |
| **Async‑first** | `Tortoise‑ORM` | ✔ | Django‑style models, asyncio only. |
| **No ORM** | `sqlite3` stdlib | ✔ | When you want raw control or extreme footprint savings. |

> **Tip** — If coming from Dapper, start with **pydapper** for minimal friction, or use **SQLModel** for stronger typing while retaining near‑SQL flexibility.

* * *

## 3. POCO‑style models & strict typing in Python

### a. Plain dataclasses

```python
from dataclasses import dataclass
from typing   import Annotated
import sqlite3, datetime as dt

@dataclass(slots=True)
class Todo:
    id:   int
    text: str
    due:  Annotated[dt.date | None, "nullable"] = None
```

* Use `slots=True` for memory efficiency (Python 3.12+).
    
* Validate in `__post_init__` or with libraries such as **dacite** or **pydantic‑dataclasses**. [Sling Academy](https://www.slingacademy.com/article/python-sqlite3-using-dataclass-to-validate-data-before-inserting/?utm_source=chatgpt.com)
    
* Convert query rows to models via a custom `row_factory`:
    

```python
def to_dataclass(cursor, row):
    return Todo(*row)

con = sqlite3.connect(":memory:")
con.row_factory = to_dataclass
```

### b. Pydantic / SQLModel (the “strongest” typing)

```python
from sqlmodel import SQLModel, Field, Session, select
class Todo(SQLModel, table=True):
    id:   int | None = Field(default=None, primary_key=True)
    text: str
    due:  dt.date | None = None
```

You get:

* Runtime validation (`.model_validate`),
    
* IDE/autocomplete support,
    
* Seamless mapping to SQLite tables (`SQLModel.metadata.create_all(engine)`).
    

* * *

## 4. Code‑First schema changes (SQLite edition)

### Option A — SQLAlchemy + Alembic (most mature)

1. **Init**
    

```bash
pip install sqlalchemy alembic sqlite-utils
alembic init alembic
```

2. **Point Alembic at SQLite**
    

`alembic.ini` → `sqlalchemy.url = sqlite:///app.db`

3. **Autogenerate migration**
    

```bash
alembic revision --autogenerate -m "Add Todo table"
alembic upgrade head
```

Alembic’s _batch mode_ transparently rewrites `ALTER TABLE` operations into the “create‑copy‑rename” pattern required by SQLite. [Alembic](https://alembic.sqlalchemy.org/en/latest/autogenerate.html?utm_source=chatgpt.com)[Alembic](https://alembic.sqlalchemy.org/en/latest/batch.html?utm_source=chatgpt.com)

### Option B — Caribou or yoyo‑migrations (SQLite‑focused)

_Caribou_ is a tiny migration runner that simply executes numbered `.sql` files and tracks version in `PRAGMA user_version`, ideal for offline or embedded deployments. [GitHub](https://github.com/clutchski/caribou?utm_source=chatgpt.com)

### Workflow parity with .NET Entity Framework

| EF Core | Python analogue |
| --- | --- |
| `Add-Migration` | `alembic revision --autogenerate` |
| `Update-Database` | `alembic upgrade head` |
| `DbContext` | SQLAlchemy `Session` / SQLModel `Session` |
| Fluent `HasOne()…WithMany()` | SQLAlchemy relationship attributes + foreign‑key columns |

* * *

## 5. SQLite‑flavoured SQL examples

| Feature | Example | Notes |
| --- | --- | --- |
| **Upsert (`ON CONFLICT`)** | `INSERT INTO users(id,name) VALUES(1,'Ann') ON CONFLICT(id) DO UPDATE SET name=excluded.name;` | Supported since 3.24 (2018). [SQLite](https://sqlite.org/lang_upsert.html?utm_source=chatgpt.com) |
| **JSON functions** | `SELECT json_extract(info,'$.email') FROM users;` | Built‑in `json1` extension gives `json_extract`, `json_set`, etc. [sqlitetutorial.net](https://www.sqlitetutorial.net/sqlite-json-functions/sqlite-json_extract-function/?utm_source=chatgpt.com) |
| **Foreign keys** | `PRAGMA foreign_keys = ON;`  
`CREATE TABLE orders(user_id INTEGER REFERENCES users(id));` | Enforcement is off by default; enable per connection. [SQLite](https://sqlite.org/foreignkeys.html?utm_source=chatgpt.com) |
| **FTS5 full‑text search** | `CREATE VIRTUAL TABLE docs USING fts5(title, body);` | Instant search without external indexer. |
| **Window functions** | `SELECT id, value, avg(value) OVER () AS avg_val FROM metrics;` | Available since 3.25. |

* * *

## 6. Putting it all together – minimal runnable stack

```python
from sqlmodel import SQLModel, Field, Session, create_engine, select
import datetime as dt

class Todo(SQLModel, table=True):
    id:   int | None = Field(default=None, primary_key=True)
    text: str
    due:  dt.date | None = None

engine = create_engine("sqlite:///app.db", echo=False)
SQLModel.metadata.create_all(engine)         # first migration

with Session(engine) as s:
    s.add(Todo(text="Write docs", due=dt.date.today()))
    s.commit()

with Session(engine) as s:
    todos = s.exec(select(Todo)).all()
    print(todos)
```

Add **Alembic** to evolve the model, and **pydapper** (or raw SQL) when you need the last drop of speed.

* * *

### Key take‑aways

1. **Version schema, not data**—keep `.db` out of Git except for static fixtures.
    
2. **Pick the right abstraction level**:  
    _Raw SQL_ → _pydapper_ → _Peewee_ → _SQLModel/SQLAlchemy_.
    
3. **Type safety is perfectly achievable** in Python 3.12+—`dataclass(slots=True)` or `SQLModel` gives you POCO‑like ergonomics.
    
4. **Alembic batch mode** delivers reliable Code‑First migrations even on SQLite’s limited DDL.
    
5. Learn SQLite’s extras (`UPSERT`, `json1`, FTS5) to unlock surprisingly powerful single‑file applications.
    

Happy coding!