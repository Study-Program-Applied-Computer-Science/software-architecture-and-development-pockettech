import uuid
from sqlalchemy import or_, and_
from sqlalchemy.orm import Session

# 1. Import your SQLAlchemy models
from app.models.transaction import Transaction as TransactionModel
from app.models.country import Country as CountryModel
from app.models.user import User as UserModel
from app.models.userTransactionsCategory import UserTransactionsCategory as UserTransactionsCategoryModel

# 2. Import your Pydantic schemas
from app.schemas.transaction import TransactionCreate, TransactionResponse, TransactionUpdate
from app.schemas.country import CountryCreate, CountryResponse
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.schemas.userTransactionsCategory import (
    UserTransactionsCategoryCreate,
    UserTransactionsCategoryResponse,
)
# ---------------------------------------------------------------------------------
# TRANSACTION CRUD
# ---------------------------------------------------------------------------------
def get_transactions(db: Session) -> list[TransactionModel]:
    """Retrieve all transactions."""
    return db.query(TransactionModel).all()

def get_transaction_by_id(db: Session, transaction_id: uuid.UUID) -> TransactionModel | None:
    """Retrieve a single transaction by its ID."""
    return db.query(TransactionModel).filter(TransactionModel.id == transaction_id).first()

def get_transaction_by_user_id(db: Session, user_id: uuid.UUID) -> list[TransactionModel]:
    """Retrieve all transactions by a user."""
    return db.query(TransactionModel).filter(
        or_(
            TransactionModel.recording_user_id == user_id,
            TransactionModel.credit_user_id == user_id,
            TransactionModel.debit_user_id == user_id
        )
    ).all()

def get_transaction_by_user_id_date(db: Session, user_id: uuid.UUID, start_date, end_date) -> list[TransactionModel]:
    """Retrieve all transactions by a user."""
    return db.query(TransactionModel).filter(
        or_(
            TransactionModel.recording_user_id == user_id,
            TransactionModel.credit_user_id == user_id,
            TransactionModel.debit_user_id == user_id
        ),
        TransactionModel.timestamp >= start_date,
        TransactionModel.timestamp <= end_date
    ).all()

def get_transaction_by_category_id(db: Session, user_id: uuid.UUID, category_id: uuid.UUID, start_date, end_date) -> list[TransactionModel]:
    """Retrieve all transactions by a user."""
    return db.query(TransactionModel).filter(
        and_(
            or_(
                TransactionModel.recording_user_id == user_id,
                TransactionModel.credit_user_id == user_id,
                TransactionModel.debit_user_id == user_id
            ),
            TransactionModel.category == category_id,
            TransactionModel.timestamp >= start_date,
            TransactionModel.timestamp <= end_date
        )
    ).all()

def create_transaction(db: Session, transaction_in: TransactionCreate) -> TransactionModel:
    """Create a new transaction record."""
    db_transaction = TransactionModel(**transaction_in.model_dump())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def update_transaction(db: Session, transaction_id: uuid.UUID, transaction_in: TransactionUpdate):
    db_transaction = db.query(TransactionModel).filter(TransactionModel.id == transaction_id).first()
    
    if not db_transaction:
        return None  # Handle missing transaction properly
    
    # Convert Pydantic model to dictionary and exclude None values
    update_data = transaction_in.model_dump(exclude_unset=True)

    # Update the database object
    for key, value in update_data.items():
        setattr(db_transaction, key, value)

    db.commit()
    db.refresh(db_transaction)
    return db_transaction



def delete_transaction(db: Session, transaction_id: uuid.UUID) -> TransactionModel | None:
    """Delete a transaction record."""
    db_transaction = db.query(TransactionModel).filter(TransactionModel.id == transaction_id).first()
    if db_transaction is None:
        return None

    db.delete(db_transaction)
    db.commit()
    return db_transaction




# # ---------------------------------------------------------------------------------
# # USER TRANSACTIONS CATEGORY CRUD
# # ---------------------------------------------------------------------------------
# def create_user_transactions_category(db: Session, category_in: UserTransactionsCategoryCreate) -> UserTransactionsCategoryModel:
#     """Create a user transactions category record."""
#     db_category = UserTransactionsCategoryModel(**category_in.dict())
#     db.add(db_category)
#     db.commit()
#     db.refresh(db_category)
#     return db_category

# def get_user_transactions_categories(db: Session) -> list[UserTransactionsCategoryModel]:
#     """Retrieve all user transaction categories."""
#     return db.query(UserTransactionsCategoryModel).all()

# def get_user_transactions_category_by_id(db: Session, category_id: uuid.UUID) -> UserTransactionsCategoryModel | None:
#     """Retrieve a single user transaction category by its ID."""
#     return db.query(UserTransactionsCategoryModel).filter(UserTransactionsCategoryModel.id == category_id).first()
 