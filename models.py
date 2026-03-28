from sqlalchemy import Column , Integer , String , Float
from database import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer , primary_key = True , index = True)
    name = Column(String , index = True)
    price = Column(Float)
    quantity = Column(Integer)


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer , primary_key = True , index = True)
    product_id = Column(Integer)  # this is for foreign key relationship with product table , but we are not implementing that in this project
    quantity = Column(Integer)


class Activity(Base):
    __tablename__ = "activities"
    id = Column(Integer , primary_key = True , index = True)
    product_id = Column(Integer)  # this is for foreign key relationship with product table , but we are not implementing that in this project
    action = Column(String)
    quantity_change = Column(Integer)




















# from pydantic import BaseModel,Field


# class Product(BaseModel):
#     id: int
#     name: str = Field(... , min_length=1)
#     price: float = Field(... , gt=0)
#     quantity: int = Field(default=0 , ge=0)


# class Order(BaseModel):
#     id : int
#     product_id : int
#     quantity : int = Field(... , gt=0)    # quantity of the product in the order  // qunatity > 0


# class Activity(BaseModel):
#     id : int
#     product_id : int
#     action : str = Field(... , min_length=1)
#     quantity_change : int    # postive for create , increase , negative for decrease , delete

