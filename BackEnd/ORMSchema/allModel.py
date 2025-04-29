from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.schema import MetaData
from ORMSchema.employee import EmployeeSchema
from ORMSchema.Vehicles import Vehicle, VehicleValidationModel

from ORMSchema.Inventory import Inventory
from ORMSchema.credentials import Credentials



DATABASE_URL = "mysql+pymysql://PrimeAssets:Prime.Assets@localhost:3306"

    # Create the database engine with connection pooling
engine = create_engine(
        DATABASE_URL,
        pool_size=10,        # Maintain 10 open connections
        max_overflow=5,      # Allow up to 5 temporary extra connections
        pool_recycle=1800,   # Reuse connections every 30 minutes
        pool_pre_ping=True   # Check connections before using
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

metadata = MetaData()
Base = declarative_base(metadata=metadata)


def get_db():
    db = SessionLocal() 
    try:
        yield db         
    finally:
        db.close()  
        


class DataBaseAccess:

    def __init__(self):
        self.createDatabase()
        self.createTables()


    def createDatabase(self):
        """Creates the required schemas if they do not exist."""
        schemas = ["credentials", "employee", "inventory", "vehicles"]
        with engine.connect() as conn:
            for schema in schemas:
                conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {schema};"))
                print(f"Schema '{schema}' created.")

    def createTables(self):
        """Creates tables in the 'credentials' schema."""

        schema_engine = create_engine(DATABASE_URL + "/credentials")
           
        self.emp = EmployeeSchema(Base)
        self.veh = Vehicle(Base)
        self.inv = Inventory(Base)
        self.crd = Credentials(Base)

        self.vehModel = VehicleValidationModel()
        
        Base.metadata.create_all(schema_engine)
        print("All tables created successfully in 'credentials' schema.")
    
 
        
