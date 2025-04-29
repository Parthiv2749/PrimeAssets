from fastapi import FastAPI, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta, timezone

import jwt
from passlib.context import CryptContext
from typing import List, Optional, Dict, Any
import uvicorn
import socket
import json

from sqlalchemy import or_, cast, Float, func
from sqlalchemy.orm import Session
from datetime import date


from ORMSchema.allModel import DataBaseAccess, get_db

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# --- Configuration ---
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15  # shorter expiry for access token
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 9  # e.g., refresh token valid for 1 day

dataAccess = DataBaseAccess()
# dataAccess.createDatabase()
# dataAccess.createTables()




fake_refresh_tokens: Dict[str, str] = {}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_hashed_password(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],         # Allows requests from any origin
    allow_credentials=True,
    allow_methods=["*"],         # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],         # Allows all headers
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
print(oauth2_scheme.scheme_name)

Inventory = InferringRouter()
Vehicle = InferringRouter()
# --- Token Endpoint for Access and Refresh Tokens ---
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    # user = dataAccess.session.query(dataAccess.crd.User).filter(dataAccess.crd.User.username == form_data.username).first() 
    user = (    db.query(dataAccess.crd.User)
    .join(dataAccess.emp.Employee, dataAccess.crd.User.employee_id == dataAccess.emp.Employee.EmployeeID)
    .filter(
        or_(
            dataAccess.crd.User.username == form_data.username,
            dataAccess.emp.Employee.Email == form_data.username  # Assuming email is stored under "Email" in Employee table
        )
    )
    .first()
    )
    
    # print(dataAccess.inv.Inventory.__table__.columns.keys())
    
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # access_token = create_access_token({"sub": user["username"], "roles": user["roles"]}, access_token_expires)
    access_token = create_access_token({"sub": user.username, "roles": "admin"}, access_token_expires)
    
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    # refresh_token = create_refresh_token({"sub": user["username"]}, refresh_token_expires)
    refresh_token = create_refresh_token({"sub": user.username}, refresh_token_expires)
    
    # Store refresh token (in a real app, save in the database)

    # fake_refresh_tokens[user["username"]] = refresh_token
    fake_refresh_tokens[user.username] = refresh_token

    return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}

# --- Refresh Token Endpoint ---
@app.post("/refresh")
async def refresh_token(refresh_token: str = Body(...), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        # Validate that the refresh token matches the stored one
        stored_refresh = fake_refresh_tokens.get(username)
        if stored_refresh != refresh_token:
            raise HTTPException(status_code=401, detail="Refresh token mismatch")
        
        # Issue a new access token
        user = db.query(dataAccess.crd.User).filter(dataAccess.crd.User.username == username).first() 
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        new_access_token = create_access_token({"sub": user.username, "roles": "admin"}, access_token_expires)
        return {"access_token": new_access_token, "token_type": "bearer"}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# --- Utility: Get Current User with Roles ---
def get_current_user(token: str = Depends(oauth2_scheme),  db: Session = Depends(get_db)) -> Dict[str, Any]:
    # print(token)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        roles: List[str] = payload.get("roles", [])
        if not username:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        
        user = db.query(dataAccess.crd.User).filter(dataAccess.crd.User.username == username).first() 
        
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        # user["roles"] = roles  # override roles from token for this example
       
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

# --- RBAC Dependency: Check if User has at Least One Required Role ---
def require_roles(required_roles: List[str]):

    def role_checker(user: dict = Depends(get_current_user)):
        
        user_roles = user.get("roles", [])
        
        if not any(role in user_roles for role in required_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User does not have one of the required roles: {required_roles}"
            )
            
        return user
    
    return role_checker

# --- Protected Endpoint: Accessible to Any Authenticated User ---
@app.get("/users/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return {"username": current_user["username"], "full_name": current_user["full_name"], "roles": current_user["roles"]}

# --- Admin-Only Endpoint ---
@app.get("/admin")
async def read_admin_data(admin_user: dict = Depends( require_roles(["admin"]) )):
    require_roles(["admin"])("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhbGljZSIsInJvbGVzIjpbImFkbWluIiwidXNlciJdLCJleHAiOjE3NDE5ODQ3MzB9.0gITosWbDk_Npki5YYfkbmC24ffFAWrvu5Nrd3JpmeU")
    # get_current_user("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhbGljZSIsInJvbGVzIjpbImFkbWluIiwidXNlciJdLCJleHAiOjE3NDE5ODM1NDF9.vALifC_uuAhxdDW-CEivPNo9FE_1JrGvtrlMByZNWjw")
    return {"message": f"Hello {admin_user['full_name']}, you have admin access."}

# --- Endpoint Accessible by Admin or Editor ---
@app.get("/manage")
async def read_manage_data(user: dict = Depends(require_roles(["admin", "editor"]))):
    return {"message": f"Hello {user['full_name']}, you have management access."}

@cbv(Inventory)
class InventoryAPI:
        
        @Inventory.get("/inventory")
        async def get_inventory(self, current_user: dict = Depends(get_current_user),  db: Session = Depends(get_db)):
            # data = dataAccess.session.query(dataAccess.inv.Inventory).all()
            
            data = (
                db.query(
                    dataAccess.inv.Product.ProductName,
                    dataAccess.inv.Product.Description,
                    dataAccess.inv.Inventory.StockQuantity,
                    cast(dataAccess.inv.Product.SellingPrice, Float)
                )
                .join(dataAccess.inv.Inventory, dataAccess.inv.Inventory.ProductID == dataAccess.inv.Product.ProductID)
            ).all()
            
            column = ['Product Name', 'Product Description', 'Product Quantity', 'Product Price']
            # print(json.dumps({"column": column, "data": [list(row) for row in data]}) )
            return json.dumps({"column": column, "data": [list(row) for row in data]})   
        

@cbv(Vehicle)
class VehicleAPI:
        
        @Vehicle.get("/vehicle")
        async def get_vehicle(self, current_user: dict = Depends(get_current_user),  db: Session = Depends(get_db)):
            # data = dataAccess.session.query(dataAccess.inv.Inventory).all()
            
            data = (
                db.query(
                    dataAccess.veh.Vehicle.VehicleRegNo,
                    dataAccess.veh.Vehicle.Make,
                    dataAccess.veh.Vehicle.Model,
                    dataAccess.veh.Vehicle.VehicleType,
                    dataAccess.veh.Vehicle.FuelType,
                   cast(dataAccess.veh.Vehicle.Mileage, Float)  
                )
                # .join(dataAccess.veh.Inventory, dataAccess.inv.Inventory.ProductID == dataAccess.inv.Product.ProductID)
            ).all()
            
            column = ['Vehicle No', 'Make', 'Model', 'Vehicle Type', 'Fuel Type', 'Mileage']
            # print(json.dumps({"column": column, "data": [list(row) for row in data]}) )
            return json.dumps({"column": column, "data": [list(row) for row in data]})   
        
        @Vehicle.get("/fuelOnModel")
        async def getFuelOnModel(self, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
           
            data = db.query(
                        dataAccess.veh.FuelConsumption.VehicleID,
                        cast(func.sum(dataAccess.veh.FuelConsumption.FuelAmount), Float)
                    ).group_by(dataAccess.veh.FuelConsumption.VehicleID).all()
            
            # column = ['Vehicle No', 'Make', 'Model', 'Vehicle Type', 'Fuel Type', 'Mileage']
          
            return json.dumps({"data": [list(row) for row in data]})  
        
        @Vehicle.get("/fuelconsumptionOverTime")    
        async def getFuelConsumptionOverTime(self, current_user: dict = Depends(get_current_user),  db: Session = Depends(get_db)):
            
            fuel_data = (
            db.query(
                dataAccess.veh.FuelConsumption.VehicleID,
                func.date_format(dataAccess.veh.FuelConsumption.FuelDate, "%Y-%m-%d"),
                cast(func.sum(dataAccess.veh.FuelConsumption.FuelAmount), Float)
            )
            .group_by(dataAccess.veh.FuelConsumption.VehicleID, func.date_format(dataAccess.veh.FuelConsumption.FuelDate, "%Y-%m-%d"))
            .order_by(dataAccess.veh.FuelConsumption.VehicleID, func.date_format(dataAccess.veh.FuelConsumption.FuelDate, "%Y-%m-%d"))
            
            ).all()
            
            return json.dumps({"data" : [list(row) for row in fuel_data]})

        @Vehicle.post("/addvehicle", response_model=dataAccess.vehModel.VehicleSchema)
        async def add_vehicle(self, vehicle: dataAccess.vehModel.VehicleSchema, current_user: dict = Depends(get_current_user),  db: Session = Depends(get_db)):
            db_vehicle = dataAccess.veh.Vehicle(**vehicle.model_dump())
            db.add(db_vehicle)
            db.commit()
            db.refresh(db_vehicle)
            return db_vehicle
            
app.include_router(Inventory)
app.include_router(Vehicle)

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

print("Your Computer Name is:" + hostname)
print("Your Computer IP Address is:" + IPAddr)

uvicorn.run(app, host=f"{IPAddr}", port=8000)

