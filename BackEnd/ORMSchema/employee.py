from sqlalchemy import  Column, Integer, String, DECIMAL, Date, Enum, ForeignKey, Text, Time
from sqlalchemy.orm import relationship

class EmployeeSchema:
    
  def __init__(self, Mainbase):
    Base = Mainbase
        
    # Employee Model
    class Employee(Base):
        __tablename__ = 'employee'
        __table_args__ = {"schema": "employee"}
        EmployeeID = Column(Integer, primary_key=True, autoincrement=True)
        FirstName = Column(String(50), nullable=False)
        LastName = Column(String(50), nullable=False)
        DateOfBirth = Column(Date, nullable=False)
        Gender = Column(Enum('Male', 'Female', 'Other'), nullable=False)
        PhoneNumber = Column(String(15))
        Email = Column(String(100), unique=True)
        Address = Column(Text)
        HireDate = Column(Date, nullable=False)
        JobID = Column(Integer, ForeignKey('employee.job.JobID'), nullable=False)
        DepartmentID = Column(Integer, ForeignKey('employee.department.DepartmentID'), nullable=False)
        Salary = Column(DECIMAL(10,2), nullable=False)
        ManagerID = Column(Integer, ForeignKey('employee.employee.EmployeeID'))
        Status = Column(Enum('Active', 'Inactive', 'Terminated'), default='Active')

        department = relationship("Department", back_populates="employees", foreign_keys=[DepartmentID])
        job = relationship("Job", back_populates="employees")
        manager = relationship("Employee", remote_side=[EmployeeID]) 

    # Department Model
    class Department(Base):
        __tablename__ = 'department'
        __table_args__ = {"schema": "employee"}
        DepartmentID = Column(Integer, primary_key=True, autoincrement=True)
        DepartmentName = Column(String(100), unique=True, nullable=False)
        ManagerID = Column(Integer, ForeignKey('employee.employee.EmployeeID')) 

        employees = relationship("Employee", back_populates="department", foreign_keys=[Employee.DepartmentID])
        manager = relationship("Employee", foreign_keys=[ManagerID])  

    # Job Model
    class Job(Base):
        __tablename__ = 'job'
        __table_args__ = {"schema": "employee"}
        JobID = Column(Integer, primary_key=True, autoincrement=True)
        JobTitle = Column(String(100), unique=True, nullable=False)
        MinSalary = Column(DECIMAL(10,2), nullable=False)
        MaxSalary = Column(DECIMAL(10,2), nullable=False)

        employees = relationship("Employee", back_populates="job")

    # Attendance Model
    class Attendance(Base):
        __tablename__ = 'attendance'
        __table_args__ = {"schema": "employee"}
        AttendanceID = Column(Integer, primary_key=True, autoincrement=True)
        EmployeeID = Column(Integer, ForeignKey('employee.employee.EmployeeID'), nullable=False)
        Date = Column(Date, nullable=False)
        CheckInTime = Column(Time, nullable=False)
        CheckOutTime = Column(Time)
        Status = Column(Enum('Present', 'Absent', 'Leave'), nullable=False, default='Present')

    # Leave Requests Model
    class LeaveRequests(Base):
        __tablename__ = 'leaverequests'
        __table_args__ = {"schema": "employee"}
        LeaveID = Column(Integer, primary_key=True, autoincrement=True)
        EmployeeID = Column(Integer, ForeignKey('employee.employee.EmployeeID'), nullable=False)
        LeaveType = Column(Enum('Sick Leave', 'Vacation', 'Personal', 'Unpaid'), nullable=False)
        StartDate = Column(Date, nullable=False)
        EndDate = Column(Date, nullable=False)
        Status = Column(Enum('Pending', 'Approved', 'Rejected'), default='Pending')

    # Performance Review Model
    class PerformanceReview(Base):
        __tablename__ = 'performancereview'
        __table_args__ = {"schema": "employee"}
        ReviewID = Column(Integer, primary_key=True, autoincrement=True)
        EmployeeID = Column(Integer, ForeignKey('employee.employee.EmployeeID'), nullable=False)
        ReviewDate = Column(Date, nullable=False)
        Rating = Column(Integer)
        Comments = Column(Text)
        ReviewerID = Column(Integer, ForeignKey('employee.EmployeeID'), nullable=False)

    # Salary History Model
    class SalaryHistory(Base):
        __tablename__ = 'salaryhistory'
        __table_args__ = {"schema": "employee"}
        SalaryID = Column(Integer, primary_key=True, autoincrement=True)
        EmployeeID = Column(Integer, ForeignKey('employee.employee.EmployeeID'), nullable=False)
        OldSalary = Column(DECIMAL(10,2), nullable=False)
        NewSalary = Column(DECIMAL(10,2), nullable=False)
        ChangeDate = Column(Date, nullable=False)

    
    self.Employee = Employee
    self.Department = Department
    self.Job = Job
    self.Attendance = Attendance
    self.LeaveRequests = LeaveRequests
    self.PerformanceReview = PerformanceReview
    self.SalaryHistory = SalaryHistory


