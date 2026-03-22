from pydantic import BaseModel,Field


class Product(BaseModel):
    id: int
    name: str = Field(... , min_length=1)
    price: float = Field(... , gt=0)
    quantity: int = Field(default=0 , ge=0)


class Order(BaseModel):
    id : int
    product_id : int
    quantity : int = Field(... , gt=0)    # quantity of the product in the order  // qunatity > 0


class Activity(BaseModel):
    id : int
    product_id : int
    action : str = Field(... , min_length=1)
    quantity_change : int    # postive for create , increase , negative for decrease , delete

