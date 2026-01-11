from fastapi import FastAPI

from books_api.db import Base, engine
from books_api.http import books_router, borrowings_router, users_router
from books_api.utils import setup_logging

logger = setup_logging()

Base.metadata.create_all(bind=engine)
logger.info("Database tables created")

app = FastAPI(title="Library API")
app.include_router(books_router)
app.include_router(users_router)
app.include_router(borrowings_router)
logger.info("Application started")
