from pydantic import BaseModel,Field


class ProductCreate(BaseModel):
    name: str = Field(... , min_length=1)
    price: float = Field(... , gt=0)
    quantity: int = Field(default=0 , ge=0)

    class Config:   ## This helps Pydantic talk to SQLAlchemy
        from_attributes = True



class OrderCreate(BaseModel):
    product_id : int
    quantity : int = Field(... , gt=0)    # quantity of the product in the order  // qunatity > 0

    class Config:  ## # This helps Pydantic talk to SQLAlchemy
        from_attributes = True



class ActivityCreate(BaseModel):
    product_id : int
    action : str = Field(... , min_length=1)
    quantity_change : int    # postive for create , increase , negative for decrease , delete

    class Config:  # # This helps Pydantic talk to SQLAlchemy
        from_attributes = True