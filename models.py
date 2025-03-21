from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

# Define the Base object
Base = declarative_base()

class FraudDetection(Base):
    __tablename__ = 'fraud_detection'

    id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_id = Column(String, nullable=False)
    payer_id = Column(String, nullable=False)
    payee_id = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    channel = Column(String)
    mode = Column(String)
    bank_code = Column(String)
    transaction_datetime = Column(DateTime, default=datetime.datetime.utcnow)
    is_fraud = Column(Boolean)
    detection_method = Column(String)
    score = Column(Float)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class FraudReporting(Base):
    __tablename__ = 'fraud_reporting'

    id = Column(Integer, primary_key=True)
    transaction_id = Column(String, nullable=False)
    reported_by = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    comment = Column(String)