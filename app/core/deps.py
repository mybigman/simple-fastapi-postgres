from app.db.session import SessionLocal


# generate database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
