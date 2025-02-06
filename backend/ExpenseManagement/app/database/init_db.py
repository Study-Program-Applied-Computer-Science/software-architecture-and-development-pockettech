from sqlalchemy.orm import Session
from app.db.database import engine, SessionLocal
from app.models.country import Country

def init_db():

    # Insert default country data if the table is empty
    with SessionLocal() as db:
        if not db.query(Country).first():
            # Add default countries
            countries = [
                Country(id=1,country="United States", currency="USD", phone_code="+1"),
                Country(id=2,country="India", currency="INR", phone_code="+91"),
                Country(id=3,country="Germany", currency="EUR", phone_code="+49")
            ]
            db.add_all(countries)
            db.commit()
            print("Inserted default country data.")
