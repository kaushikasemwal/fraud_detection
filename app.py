from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
import joblib
import pandas as pd

# Define the FastAPI app
app = FastAPI()

# Define the Base object
Base = declarative_base()

# Define the FraudDetection table
class FraudDetection(Base):
    __tablename__ = 'fraud_detection'

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, nullable=False)
    payer_id = Column(String, nullable=False)
    payee_id = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    channel = Column(String)
    mode = Column(String)
    bank_code = Column(String)
    transaction_datetime = Column(DateTime, default=datetime.utcnow)
    is_fraud_predicted = Column(Boolean)
    fraud_score = Column(Float)
    detection_method = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///fraud_system.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables in the database (if they don't exist)
Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Load the pre-trained model
model = joblib.load("fraud_model.pkl")

# Pydantic model for request body
class Transaction(BaseModel):
    transaction_id: str
    payer_id: str
    payee_id: str
    amount: float
    channel: str
    mode: str
    bank_code: str
    transaction_datetime: datetime

# Fraud detection endpoint
@app.post("/api/v1/detect")
def detect_fraud(tx: Transaction, db: Session = Depends(get_db)):
    try:
        # Preprocess input data
        input_data = pd.DataFrame([{
            "amount": tx.amount,
            "channel": 1 if tx.channel == "Online" else 0,
            "mode": 1 if tx.mode == "Credit Card" else 0,
            "bank_code": 1 if tx.bank_code == "Bank A" else 0
        }])

        # Predict using the model
        fraud_score = model.predict_proba(input_data)[0][1]  # Probability of fraud
        is_fraud_predicted = fraud_score > 0.5  # Binary decision

        # Store input and prediction in the database
        db_transaction = FraudDetection(
            transaction_id=tx.transaction_id,
            payer_id=tx.payer_id,
            payee_id=tx.payee_id,
            amount=tx.amount,
            channel=tx.channel,
            mode=tx.mode,
            bank_code=tx.bank_code,
            transaction_datetime=tx.transaction_datetime,
            is_fraud_predicted=is_fraud_predicted,
            fraud_score=fraud_score,
            detection_method="AI"
        )
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)

        # Return the prediction
        return {
            "transaction_id": tx.transaction_id,
            "is_fraud_predicted": is_fraud_predicted,
            "fraud_score": fraud_score,
            "message": "Fraud detection complete"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))