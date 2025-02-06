from sqlalchemy.orm import Session
from app.db.database import engine, SessionLocal
from app.models.country import Country
from app.models.transactionsCategory import TransactionsCategory

def init_db():

    # Insert default country data if the table is empty
    with SessionLocal() as db:
        if not db.query(Country).first():
            # Add default countries
            countries = [
                Country(id=1,country="United States", currency="USD", phone_code="+1"),
                Country(id=2,country="India", currency="INR", phone_code="+91"),
            ]
            db.add_all(countries)
            db.commit()
            print("Inserted default country data.")
        if not db.query(TransactionsCategory).first():
            transactionsCategories = [
                TransactionsCategory(id=1, category="Groceries", expense=True),
                TransactionsCategory(id=2, category="Clothes", expense=True),
                TransactionsCategory(id=3, category="Entertainment", expense=True),
                TransactionsCategory(id=4, category="Savings", expense=False)
            ]
            db.add_all(transactionsCategories)
            db.commit()
            print("Inserted default transactions category data.")