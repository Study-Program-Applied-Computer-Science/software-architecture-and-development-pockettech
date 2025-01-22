from app.db.database import Base, engine
from app.models.models import OCRResult

# Create all tables
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")
