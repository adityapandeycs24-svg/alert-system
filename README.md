# Captain Hawkeye Backend - Alert Module (Dev 3)

## Overview
FastAPI backend Alert module for Captain Hawkeye, managing vehicle blacklist tracking, alert feed, and trajectory integration seams.

## Project Structure
```
captain-hawkeye-backend/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── alerts/
│   │   ├── __init__.py
│   │   ├── router.py
│   │   ├── schemas.py
│   │   ├── models.py
│   │   ├── repository.py
│   │   ├── service.py
│   │   └── interfaces.py
│   ├── anpr/
│   │   └── __init__.py
│   ├── trajectory/
│   │   └── __init__.py
│   └── core/
│       ├── errors.py
│       └── time.py
├── tests/
│   ├── conftest.py
│   └── alerts/
│       ├── test_router_search.py
│       ├── test_router_feed.py
│       ├── test_router_acknowledge.py
│       ├── test_router_blacklist.py
│       └── test_service.py
├── requirements.txt
└── README.md
```

## Running the Application
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start dev server:
   ```bash
   uvicorn app.main:app --reload
   ```

## Running Tests
Run pytest to verify contract compliance:
```bash
pytest
```
