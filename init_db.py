from sqlalchemy import create_engine
from models import Base

# Create a SQLite database engine
engine = create_engine('sqlite:///fraud_system.db')

# Create all tables defined in Base
Base.metadata.create_all(engine)

print("Database and tables created successfully.")