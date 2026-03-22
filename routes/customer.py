from fastapi import APIRouter
from data import products_list, activities_list,orders_list , order_id_counter , activity_id_counter
from models import Activity,Order

router = APIRouter()


@router.post("/orders")
def order_product(given_product_id : int , order_quantity : int):
    
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





@router.get("/orders")
def get_orders(given_product_id : int = None):    # suppose in product_list --> oneproduct ::  which is high selling product : {5,zyro ,price : 60 , quanttity : 200}  ,, for this product we have 3 orders : order1 : {50 quantity} , order2 : {20 quantity}  ,, order3 : {30 quantity} 
                                                         #  having the product id :  5

    if given_product_id is not None:            # so i want to check from prduct ( from prd id how much orders)

        resultorder = [oneorder for oneorder in orders_list if oneorder.product_id == given_product_id]
        return resultorder

    return orders_list