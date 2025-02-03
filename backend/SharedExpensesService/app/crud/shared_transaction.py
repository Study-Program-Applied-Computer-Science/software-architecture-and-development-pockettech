from sqlalchemy.orm import Session
from app.models.shared_transaction import SharedTransaction
from app.models.shared_group_participants import SharedGroupParticipants
from app.schemas.shared_transaction import SharedTransactionCreate
from app.schemas.shared_group_participants import SharedGroupParticipantsBase
from app.crud.payment_status import get_payment_status
from uuid import UUID
from uuid import uuid4
from app.models.transaction import Transaction
from typing import Optional
from decimal import Decimal
from app.schemas.transaction import TransactionCreate   
from sqlalchemy import Numeric, Float

# TODO: use transaction service to create the transaction
def create_transaction(db: Session, transaction_in: TransactionCreate) -> Transaction:
    """Create a new transaction record."""
    db_transaction = Transaction(**transaction_in.model_dump())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    print(db_transaction.id)
    return db_transaction.id

# Create a shared transaction and split among group members
def create_shared_transaction(db: Session, new_transaction: Transaction) -> list[SharedTransaction]:
    """Creates shared transactions by splitting the amount among group members."""

    new_transaction.shared_transaction = True 
    new_transaction_id = create_transaction(
        db=db,
        transaction_in=new_transaction
    )

    # Get group_id of the user
    group_record = db.query(SharedGroupParticipants).filter(
        SharedGroupParticipants.participant_user_id == new_transaction.recording_user_id
    ).first()
    print(group_record.group_id)

    if not group_record:
        raise ValueError("User does not belong to any group")

    group_id = group_record.group_id  

    #  Get all users in the group (excluding the recording user)
    group_users = db.query(SharedGroupParticipants.participant_user_id).filter(
        SharedGroupParticipants.group_id == group_id
    ).all()

    group_users_list = [user.participant_user_id for user in group_users if user.participant_user_id != new_transaction.recording_user_id]

    if not group_users_list:
        raise ValueError("No other users found in the group")

    # Calculate shared amount per user
    split_amount = new_transaction.amount / len(group_users_list)

    pending_payment_status = get_payment_status(db)["pending"]

    new_shared_transactions = []
    for user_id in group_users_list:
        shared_transaction = SharedTransaction(
            transaction_id=new_transaction_id,
            group_user_id_main=new_transaction.recording_user_id,  # ✅ Corrected
            group_user_id_sub=user_id,
            share_value=split_amount,
            payment_status= pending_payment_status
        )
        db.add(shared_transaction)
        new_shared_transactions.append(shared_transaction)

    db.commit()  # Commit after adding all shared transactions

    return new_shared_transactions  # Return the list of shared transactions


# Update the repayment transaction ID and payment_status in the SharedTransaction record
def update_repayment_transaction(
    db: Session,
    shared_transaction_id: UUID
):
    shared_transaction = db.query(SharedTransaction).filter(SharedTransaction.id == shared_transaction_id).first()

    if not shared_transaction:
        raise ValueError(f"Shared transaction with ID {shared_transaction_id} not found.")

    # TODO: use transaction service to get the transaction
    transaction = db.query(Transaction).filter(Transaction.id == shared_transaction.transaction_id).first()

    if not transaction:
        raise ValueError(f"Transaction with ID {shared_transaction.transaction_id} not found.")
    
    repayment = TransactionCreate(
        recording_user_id=shared_transaction.group_user_id_sub,
        credit_user_id=shared_transaction.group_user_id_main,
        debit_user_id=shared_transaction.group_user_id_sub,
        amount=shared_transaction.share_value,
        category=transaction.category,
        currency_code=transaction.currency_code,
        heading="Repayment",
        transaction_mode="repayment",
        shared_transaction=False
    )
    repayment_transaction_id = create_transaction(
        db=db,
        transaction_in=repayment
    )

    payment_status_values = get_payment_status(db)
    paid_payment_status = payment_status_values["completed"]
    if paid_payment_status is None:
        raise ValueError("Payment status 'completed' not found.")
    
    if repayment_transaction_id:
        # Update repayment_transaction_id to the new payment transaction
        shared_transaction.repayment_transaction_id = repayment_transaction_id
        shared_transaction.payment_status = paid_payment_status
        db.commit()
        db.refresh(shared_transaction)
    
    return shared_transaction


# Create a repayment transaction
def create_repayment_transaction(
    db: Session,
    recording_user_id: UUID,
    credit_user_id: UUID,
    debit_user_id: UUID,
    amount: Float,
    category: int,
    currency_code: int,
    heading: str,
    description: Optional[str]
) -> Transaction:
    repayment_transaction = create_transaction(
        db=db,
        recording_user_id=recording_user_id,
        credit_user_id=credit_user_id,
        debit_user_id=debit_user_id,
        amount=amount,
        category=category,
        currency_code=currency_code,
        heading=heading,
        description=description,
        transaction_mode="repayment",  # Mark as a repayment
        shared_transaction=False  # Normal transaction
    )
    return repayment_transaction

# get transaction by group_user_id_main or group_user_id_sub
def get_transaction_by_group_user_id(
    db: Session,
    group_user_id: UUID
) -> list[SharedTransaction]:
    shared_transactions = db.query(SharedTransaction).filter(
        (SharedTransaction.group_user_id_main == group_user_id) | (SharedTransaction.group_user_id_sub == group_user_id)
    ).all()
    return shared_transactions