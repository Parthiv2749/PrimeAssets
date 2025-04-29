from sqlalchemy import (Column, Integer, String, DECIMAL, Enum, Date, Text, ForeignKey, TIMESTAMP)
from sqlalchemy.orm import relationship
from pydantic import BaseModel, condecimal
from datetime import date, datetime
from typing import Optional

class Vehicle:

  def __init__(self, Mainbase):
    Base = Mainbase

    # Vehicle Model (Define First)
    class VehicleCategory(Base):
        __tablename__ = 'vehiclecategories'
        __table_args__ = {"schema": "vehicles"}

        CategoryID = Column(Integer, primary_key=True, autoincrement=True)
        CategoryName = Column(String(100), nullable=False)
        Description = Column(Text, nullable=True)
        vehicles = relationship("Vehicle", back_populates="category", cascade="all, delete")
  
    # Vehicles Table
    class Vehicle(Base):
        __tablename__ = 'vehicles'
        __table_args__ = {"schema": "vehicles"}

        VehicleID = Column(Integer, primary_key=True, autoincrement=True)
        VehicleRegNo = Column(String(50), nullable=False, unique=True)
        Make = Column(String(100), nullable=False)
        Model = Column(String(100), nullable=True)
        VehicleType = Column(Enum('Sedan', 'SUV', 'Truck', 'Van', 'Motorcycle', 'Other'), nullable=False)
        FuelType = Column(Enum('Petrol', 'Diesel', 'Electric', 'Hybrid'), nullable=False)
        EngineCapacity = Column(DECIMAL(5,2), nullable=True)
        Mileage = Column(DECIMAL(10,2), nullable=False)
        Status = Column(Enum('Active', 'Inactive', 'Under Maintenance', 'Decommissioned'), default='Active')
        LastServiced = Column(Date, nullable=True)
        CategoryID = Column(Integer, ForeignKey('vehicles.vehiclecategories.CategoryID', ondelete="CASCADE"), nullable=False)
        category = relationship("VehicleCategory", back_populates="vehicles")
    
        # category = relationship("VehicleCategory", back_populates="vehicles")
   
    # Fuel Consumption Table
    class FuelConsumption(Base):
        __tablename__ = 'fuelconsumption'
        __table_args__ = {"schema": "vehicles"}

        FuelID = Column(Integer, primary_key=True, autoincrement=True)
        VehicleID = Column(Integer, ForeignKey('vehicles.vehicles.VehicleID'), nullable=False)
        FuelDate = Column(TIMESTAMP, nullable=True)
        FuelAmount = Column(DECIMAL(10,2), nullable=False)
        FuelCost = Column(DECIMAL(10,2), nullable=False)
        OdometerReading = Column(DECIMAL(10,2), nullable=False)
        FuelStation = Column(String(100), nullable=True)

    # Vehicle Assignment Table
    class VehicleAssignment(Base):
        __tablename__ = 'vehicleassignments'
        __table_args__ = {"schema": "vehicles"}

        AssignmentID = Column(Integer, primary_key=True, autoincrement=True)
        VehicleID = Column(Integer, ForeignKey('vehicles.vehicles.VehicleID'), nullable=False)
        EmployeeID = Column(Integer, ForeignKey('employee.employee.EmployeeID'), nullable=False)
        AssignmentDate = Column(TIMESTAMP, nullable=True)
        ReturnDate = Column(Date, nullable=True)
        Status = Column(Enum('Assigned', 'Returned', 'In Use', 'Inactive'), default='Assigned')
        Comments = Column(Text, nullable=True)

    # Vehicle Inspection Table
    class VehicleInspection(Base):
        __tablename__ = 'vehicleinspections'
        __table_args__ = {"schema": "vehicles"}

        InspectionID = Column(Integer, primary_key=True, autoincrement=True)
        VehicleID = Column(Integer, ForeignKey('vehicles.vehicles.VehicleID'), nullable=False)
        InspectionDate = Column(TIMESTAMP, nullable=True)
        InspectorName = Column(String(100), nullable=True)
        InspectionType = Column(Enum('Safety', 'Emissions', 'Regulatory'), nullable=True)
        Status = Column(Enum('Passed', 'Failed', 'Pending'), default='Pending')
        Comments = Column(Text, nullable=True)

    # Vehicle Maintenance Table
    class VehicleMaintenance(Base):
        __tablename__ = 'vehiclemaintenance'
        __table_args__ = {"schema": "vehicles"}

        MaintenanceID = Column(Integer, primary_key=True, autoincrement=True)
        VehicleID = Column(Integer, ForeignKey('vehicles.vehicles.VehicleID'), nullable=False)
        MaintenanceDate = Column(TIMESTAMP, nullable=True)
        Type = Column(Enum('Routine', 'Repair', 'Emergency'), nullable=False)
        Status = Column(Enum('Scheduled', 'Completed', 'Cancelled'), default='Scheduled')
        Description = Column(Text, nullable=True)
        Cost = Column(DECIMAL(10,2), nullable=True)
        NextMaintenanceDate = Column(Date, nullable=True)

    # Vehicle Usage Table
    class VehicleUsage(Base):
        __tablename__ = 'vehicleusage'
        __table_args__ = {"schema": "vehicles"}

        UsageID = Column(Integer, primary_key=True, autoincrement=True)
        VehicleID = Column(Integer, ForeignKey('vehicles.vehicles.VehicleID'), nullable=False)
        EmployeeID = Column(Integer, ForeignKey('employee.employee.EmployeeID'), nullable=False)
        UsageDate = Column(TIMESTAMP, nullable=True)
        DistanceTraveled = Column(DECIMAL(10,2), nullable=False)
        Purpose = Column(Text, nullable=True)
    # Store class references

    self.VehicleCategory = VehicleCategory
    self.VehicleInspection = VehicleInspection
    self.VehicleMaintenance = VehicleMaintenance
    self.VehicleAssignment = VehicleAssignment
    self.VehicleUsage = VehicleUsage
    self.Vehicle = Vehicle
    self.FuelConsumption = FuelConsumption
        
# Pydantic Models

class VehicleValidationModel:

    class VehicleCategorySchema(BaseModel):
        CategoryID: int
        CategoryName: str
        Description: Optional[str] = None

        class Config:
            from_attributes = True


    # Vehicle Schema
    class VehicleSchema(BaseModel):
        # VehicleID: int
        VehicleRegNo: str
        Make: str
        Model: Optional[str] = None
        VehicleType: str
        FuelType: str
        EngineCapacity: Optional[condecimal(max_digits=5, decimal_places=2)] = None
        Mileage: condecimal(max_digits=10, decimal_places=2)
        Status: str
        LastServiced: Optional[date] = None
        CategoryID: int

        class Config:
            from_attributes = True


    # Fuel Consumption Schema
    class FuelConsumptionSchema(BaseModel):
        FuelID: int
        VehicleID: int
        FuelDate: Optional[datetime] = None
        FuelAmount: condecimal(max_digits=10, decimal_places=2)
        FuelCost: condecimal(max_digits=10, decimal_places=2)
        OdometerReading: condecimal(max_digits=10, decimal_places=2)
        FuelStation: Optional[str] = None

        class Config:
            from_attributes = True


    # Vehicle Assignment Schema
    class VehicleAssignmentSchema(BaseModel):
        AssignmentID: int
        VehicleID: int
        EmployeeID: int
        AssignmentDate: Optional[datetime] = None
        ReturnDate: Optional[date] = None
        Status: str
        Comments: Optional[str] = None

        class Config:
            from_attributes = True


    # Vehicle Inspection Schema
    class VehicleInspectionSchema(BaseModel):
        InspectionID: int
        VehicleID: int
        InspectionDate: Optional[datetime] = None
        InspectorName: Optional[str] = None
        InspectionType: Optional[str] = None
        Status: str
        Comments: Optional[str] = None

        class Config:
            from_attributes = True


    # Vehicle Maintenance Schema
    class VehicleMaintenanceSchema(BaseModel):
        MaintenanceID: int
        VehicleID: int
        MaintenanceDate: Optional[datetime] = None
        Type: str
        Status: str
        Description: Optional[str] = None
        Cost: Optional[condecimal(max_digits=10, decimal_places=2)] = None
        NextMaintenanceDate: Optional[date] = None

        class Config:
            from_attributes = True


    # Vehicle Usage Schema
    class VehicleUsageSchema(BaseModel):
        UsageID: int
        VehicleID: int
        EmployeeID: int
        UsageDate: Optional[datetime] = None
        DistanceTraveled: condecimal(max_digits=10, decimal_places=2)
        Purpose: Optional[str] = None

        class Config:
            from_attributes = True