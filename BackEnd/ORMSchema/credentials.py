from sqlalchemy import Column, BigInteger, String, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field
from sqlalchemy import text 
 


class Credentials:
    

  def __init__(self, Mainbase):
    Base = Mainbase

    class Permission(Base):
        __tablename__ = 'permissions'
        __table_args__ = {"schema": "credentials"}

        id = Column(BigInteger, primary_key=True, autoincrement=True)
        permission_name = Column(String(100), unique=True, nullable=False)

    class Role(Base):
        __tablename__ = 'roles'
        __table_args__ = {"schema": "credentials"}

        id = Column(BigInteger, primary_key=True, autoincrement=True)
        role_name = Column(String(50), unique=True, nullable=False)

    class RolePermission(Base):
        __tablename__ = 'role_permissions'
        __table_args__ = {"schema": "credentials"}

        role_id = Column(Integer, primary_key=True)
        permission_id = Column(Integer, primary_key=True)

    class UserRole(Base):
        __tablename__ = 'user_roles'
        __table_args__ = {"schema": "credentials"}

        user_id = Column(Integer, primary_key=True)
        role_id = Column(Integer, primary_key=True)

    class User(Base):
        __tablename__ = 'users'
        __table_args__ = {"schema": "credentials"}

        id = Column(BigInteger, primary_key=True, autoincrement=True)
        username = Column(String(100), unique=True, nullable=False)
        employee_id = Column(Integer, ForeignKey('employee.employee.EmployeeID'), unique=True, nullable=False)
        password_hash = Column(Text, nullable=False)

    self.Permission = Permission
    self.Role = Role
    self.RolePermission = RolePermission
    self.UserRole = UserRole
    self.User = User
# pydentic Validation 

class user(BaseModel):
    username: str
    password: str
    employee_id: int
    
    class Config:
        from_attributes = True

