import uuid
from sqlalchemy.orm import Session

# 1. Import your SQLAlchemy models
from app.models.transaction import Transaction as TransactionModel
from app.models.country import Country as CountryModel
from app.models.user import User as UserModel
from app.models.userTransactionsCategory import UserTransactionsCategory as UserTransactionsCategoryModel

# 2. Import your Pydantic schemas
from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.schemas.country import CountryCreate, CountryResponse
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.schemas.userTransactionsCategory import (
    UserTransactionsCategoryCreate,
    UserTransactionsCategoryResponse,
)
# ---------------------------------------------------------------------------------
# TRANSACTION CRUD
# ---------------------------------------------------------------------------------
def create_transaction(db: Session, transaction_in: TransactionCreate) -> TransactionModel:
    """Create a new transaction record."""
    db_transaction = TransactionModel(**transaction_in.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def get_transactions(db: Session) -> list[TransactionModel]:
    """Retrieve all transactions."""
    return db.query(TransactionModel).all()

def get_transaction_by_id(db: Session, transaction_id: uuid.UUID) -> TransactionModel | None:
    """Retrieve a single transaction by its ID."""
    return db.query(TransactionModel).filter(TransactionModel.id == transaction_id).first()

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
 