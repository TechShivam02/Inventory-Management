from database import engine, Base
import models
from fastapi import FastAPI

# 1. Import all your route files
from routes import product, customer, activity

# Create the tables
Base.metadata.create_all(bind=engine)  # this line will create the tables in the database file (inventory.db) based on the models we have defined in models.py

app = FastAPI(title="Inventory Management System")


# 2. Organize them by who uses them
app.include_router(product.router, tags=["Seller: Product Management"])
app.include_router(customer.router, tags=["Customer: Orders"])
app.include_router(activity.router, tags=["Manager: Audit Logs"])


@app.get("/")
def home():
    return {"message": "Welcome to the Inventory Management System!!!"}



