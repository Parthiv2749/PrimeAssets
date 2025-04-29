from sqlalchemy import (
    Column, Integer, String, Text, DECIMAL, Enum, ForeignKey, Date, TIMESTAMP
)
from sqlalchemy.orm import relationship
from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class Inventory:

  def __init__(self, Mainbase):
    Base = Mainbase
        



    class Category(Base):
        __tablename__ = 'categories'
        __table_args__ = {"schema": "inventory"}

        CategoryID = Column(Integer, primary_key=True, autoincrement=True)
        CategoryName = Column(String(100), unique=True, nullable=False)
        Description = Column(Text, nullable=True)

    class Customer(Base):
        __tablename__ = 'customers'
        __table_args__ = {"schema": "inventory"}

        CustomerID = Column(Integer, primary_key=True, autoincrement=True)
        CustomerName = Column(String(100), nullable=False)
        Phone = Column(String(20), nullable=True)
        Email = Column(String(100), nullable=True)
        Address = Column(Text, nullable=True)

    class Supplier(Base):
        __tablename__ = 'suppliers'
        __table_args__ = {"schema": "inventory"}

        SupplierID = Column(Integer, primary_key=True, autoincrement=True)
        SupplierName = Column(String(100), nullable=False)
        ContactName = Column(String(100), nullable=True)
        Phone = Column(String(20), nullable=True)
        Email = Column(String(100), nullable=True)
        Address = Column(Text, nullable=True)

    class Product(Base):
        __tablename__ = 'products'
        __table_args__ = {"schema": "inventory"}

        ProductID = Column(Integer, primary_key=True, autoincrement=True)
        ProductName = Column(String(100), nullable=False)
        CategoryID = Column(Integer, ForeignKey('inventory.categories.CategoryID'), nullable=False)
        SupplierID = Column(Integer, ForeignKey('inventory.suppliers.SupplierID'), nullable=False)
        PurchasePrice = Column(DECIMAL(10,2), nullable=False)
        SellingPrice = Column(DECIMAL(10,2), nullable=False)
        StockQuantity = Column(Integer, default=0, nullable=False)
        Description = Column(Text, nullable=True)

        category = relationship("Category")
        supplier = relationship("Supplier")

    class Warehouse(Base):
        __tablename__ = 'warehouses'
        __table_args__ = {"schema": "inventory"}

        WarehouseID = Column(Integer, primary_key=True, autoincrement=True)
        WarehouseName = Column(String(100), unique=True, nullable=False)
        Location = Column(String(100), nullable=True)
        ContactPerson = Column(String(100), nullable=True)
        Phone = Column(String(20), nullable=True)
        Email = Column(String(100), nullable=True)
        CreatedAt = Column(TIMESTAMP, nullable=True)

    class Inventory(Base):
        __tablename__ = 'inventory'
        __table_args__ = {"schema": "inventory"}

        InventoryID = Column(Integer, primary_key=True, autoincrement=True)
        ProductID = Column(Integer, ForeignKey('inventory.products.ProductID'), nullable=False)
        WarehouseID = Column(Integer, ForeignKey('inventory.warehouses.WarehouseID'), nullable=False)
        StockQuantity = Column(Integer, default=0, nullable=False)
        ReorderLevel = Column(Integer, default=5, nullable=False)

        product = relationship("Product")
        warehouse = relationship("Warehouse")

    class InventoryLog(Base):
        __tablename__ = 'inventorylogs'
        __table_args__ = {"schema": "inventory"}

        LogID = Column(Integer, primary_key=True, autoincrement=True)
        ProductID = Column(Integer, ForeignKey('inventory.products.ProductID'), nullable=False)
        ChangeType = Column(Enum('Purchase', 'Sale', 'Adjustment'), nullable=False)
        QuantityChanged = Column(Integer, nullable=False)

        product = relationship("Product")

    class Purchase(Base):
        __tablename__ = 'purchases'
        __table_args__ = {"schema": "inventory"}

        PurchaseID = Column(Integer, primary_key=True, autoincrement=True)
        SupplierID = Column(Integer, ForeignKey('inventory.suppliers.SupplierID'), nullable=False)
        PurchaseDate = Column(Date, nullable=False)
        TotalAmount = Column(DECIMAL(10,2), nullable=False)
        Status = Column(Enum('Pending', 'Completed', 'Cancelled'), default='Pending')

        supplier = relationship("Supplier")
    
    class PurchaseDetail(Base):
        __tablename__ = 'purchasedetails'
        __table_args__ = {"schema": "inventory"}

        PurchaseDetailID = Column(Integer, primary_key=True, autoincrement=True)
        PurchaseID = Column(Integer, ForeignKey('inventory.purchases.PurchaseID', ondelete='CASCADE'), nullable=False)
        ProductID = Column(Integer, ForeignKey('inventory.products.ProductID', ondelete='CASCADE'), nullable=False)
        Quantity = Column(Integer, nullable=False)
        UnitPrice = Column(DECIMAL(10,2), nullable=False)
        TotalPrice = Column(DECIMAL(10,2), nullable=False)

        purchase = relationship("Purchase")
        product = relationship("Product")

    class Sale(Base):
        __tablename__ = 'sales'
        __table_args__ = {"schema": "inventory"}

        SaleID = Column(Integer, primary_key=True, autoincrement=True)
        CustomerID = Column(Integer, ForeignKey('inventory.customers.CustomerID'), nullable=False)
        SaleDate = Column(Date, nullable=False)
        TotalAmount = Column(DECIMAL(10,2), nullable=False)
        PaymentStatus = Column(Enum('Pending', 'Paid', 'Refunded'), default='Pending')

        customer = relationship("Customer")

    class SaleDetail(Base):
        __tablename__ = 'saledetails'
        __table_args__ = {"schema": "inventory"}

        SaleDetailID = Column(Integer, primary_key=True, autoincrement=True)
        SaleID = Column(Integer, ForeignKey('inventory.sales.SaleID', ondelete='CASCADE'), nullable=False)
        ProductID = Column(Integer, ForeignKey('inventory.products.ProductID', ondelete='CASCADE'), nullable=False)
        WarehouseID = Column(Integer, ForeignKey('inventory.warehouses.WarehouseID', ondelete='CASCADE'), nullable=False)
        Quantity = Column(Integer, nullable=False)
        UnitPrice = Column(DECIMAL(10,2), nullable=False)
        TotalPrice = Column(DECIMAL(10,2), nullable=False)

        sale = relationship("Sale")
        product = relationship("Product")
        warehouse = relationship("Warehouse")

        self.Category = Category
        self.Customer = Customer
        self.Inventory = Inventory
        self.InventoryLog = InventoryLog
        self.Product = Product
        self.Supplier = Supplier
        self.Warehouse = Warehouse
    
    self.Category = Category
    self.Customer = Customer
    self.Inventory = Inventory
    self.InventoryLog = InventoryLog
    self.Product = Product
    self.Supplier = Supplier
    self.Warehouse = Warehouse
    self.Purchase = Purchase
    self.PurchaseDetail = PurchaseDetail
    self.Sale = Sale
    self.SaleDetail = SaleDetail
    
        
# Pydantic Schemas
class CategorySchema(BaseModel):
    categoryId: Optional[int]
    categoryName: str
    description: Optional[str]

class CustomerSchema(BaseModel):
    customerId: Optional[int]
    customerName: str
    contactName: Optional[str]
    address: Optional[str]
    city: Optional[str]
    postalCode: Optional[str]
    country: Optional[str]
    phone: Optional[str]

class InventorySchema(BaseModel):
    inventoryId: Optional[int]
    productId: int
    warehouseId: int
    quantity: int

class InventoryLogSchema(BaseModel):
    logId: Optional[int]
    inventoryId: int
    changeQuantity: int
    logDate: Optional[datetime]

class ProductSchema(BaseModel):
    productId: Optional[int]
    productName: str
    supplierId: Optional[int]
    categoryId: Optional[int]
    quantityPerUnit: Optional[str]
    unitPrice: Optional[float]
    unitsInStock: Optional[int]

class SupplierSchema(BaseModel):
    supplierId: Optional[int]
    supplierName: str
    contactName: Optional[str]
    address: Optional[str]
    city: Optional[str]
    postalCode: Optional[str]
    country: Optional[str]
    phone: Optional[str]

class WarehouseSchema(BaseModel):
    warehouseId: Optional[int]
    warehouseName: str
    location: Optional[str]