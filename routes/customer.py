from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models


router = APIRouter()


@router.post("/orders")
def order_product(given_product_id : int , order_quantity : int , db:Session = Depends(get_db)):
    
# 1. Basic Validation
    if order_quantity <=0:
        return {"message": "Order quantity is not valid one"}

# 2. Find Product
    current_product = db.query(models.Product).get(given_product_id)

    if current_product is None:
        return {"message": "Product not found"}

# 3. Check Stock
    if order_quantity <= current_product.quantity:
        

        # Deduct the Stock (SQLAlchemy tracks this automatically!)
        stock_left = current_product.quantity - order_quantity

# 4. Perform the Transaction
# Create the Order
        createOrder = models.Order(
             product_id = given_product_id,
             quantity=order_quantity
        )

        db.add(createOrder)
        
        current_product.quantity = stock_left

# Log the Activity
        latestactivity = models.Activity(
             
            product_id=given_product_id,
            action = "ORDER_PLACED",
            quantity_change=-order_quantity   # here order Q , bcz if total : 10 , order : 7 , left : 3   ,, so in activity : {"ORDERED" 7 }
        )

        db.add(latestactivity)


# 5. Save everything
        db.commit()
        db.refresh(createOrder)   # here we refresh , bcz we need the id of  "createOrder" in the response in the same block
        
        return {
            "message" : "Order placed successfully",
            "Order_details" : createOrder}

                
        
    else:
        return {"message" : "Ordered quantity is not Available"}

        
    





    """
    
    global activity_id_counter
    global order_id_counter

    if order_quantity <=0:
        return {"message": "Order quantity is not valid one"}

    for oneproduct in products_list:


        if oneproduct.id == given_product_id: #means the product exist in our db (list)

            if order_quantity <= oneproduct.quantity:  # the quantatity of order is less than or equal to present order Q -> then order


                stock_left = oneproduct.quantity - order_quantity
                

                latestorder = Order(
                    id=order_id_counter,
                    product_id = given_product_id,
                    quantity=order_quantity
                )

                orders_list.append(latestorder)
                order_id_counter+=1


                oneproduct.quantity = stock_left



                latestactivity = Activity(
                    id = activity_id_counter,
                    product_id=given_product_id,
                    action = "ORDER_PLACED",
                    quantity_change=-order_quantity   # here order Q , bcz if total : 10 , order : 7 , left : 3   ,, so in activity : {"ORDERED" 7 }
                    )
                activities_list.append(latestactivity)
                activity_id_counter+=1




                return {"Order_details" : latestorder}

                
            else:
                return {"message" : "Ordered quantity is not Available"}

        
    return {"message": "Product not found"}

        
"""





@router.get("/orders")
def get_orders(given_product_id : int = None , db:Session=Depends(get_db)):    # suppose in product_list --> oneproduct ::  which is high selling product : {5,zyro ,price : 60 , quanttity : 200}  ,, for this product we have 3 orders : order1 : {50 quantity} , order2 : {20 quantity}  ,, order3 : {30 quantity} 
                                                         #  having the product id :  5



    if given_product_id is not None:

        result_allorder = db.query(models.Order).filter(models.Order.product_id == given_product_id).all()  # this will give all the orders for the given product id
        return result_allorder
    

    allorders = db.query(models.Order).all()  # this will give all the orders in the database
    return allorders


# this below little code is for understanding the above code in simple way without using sql alchemy and database , we are using list to store the data in memory and then we are filtering the data from the list based on the given product id and then returning the result as a list of orders for that product id or all orders if product id is not given

"""
    query = db.query(models.Order)

    if given_product_id is not None:
        query = query.filter(models.Order.product_id == given_product_id)

    return query.all()  # this will give all the orders for the given product id if given_product_id is not None , otherwise it will give all the orders in the database

"""


    # if given_product_id is not None:            # so i want to check from prduct ( from prd id how much orders)

    #     resultorder = [oneorder for oneorder in orders_list if oneorder.product_id == given_product_id]
    #     return resultorder

    # return orders_list

