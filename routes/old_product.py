from fastapi import APIRouter
from data import products_list, activities_list, product_id_counter , activity_id_counter
from models import Product, Activity



router = APIRouter()



@router.post("/products")
def add_product(oneproduct : Product):
    
    global product_id_counter
    global activity_id_counter
    
    oneproduct.id = product_id_counter    # very imp step

    products_list.append(oneproduct)

    product_id_counter +=1

    latestactivity = Activity(
        id = activity_id_counter,
        product_id=oneproduct.id,
        action="CREATED",
        quantity_change=oneproduct.quantity
    )


    activities_list.append(latestactivity)

    activity_id_counter +=1    # very imp step

    return oneproduct





                            # VERY IMP :: get all the products   // LIKE the FILTER one (if have to get by product name  and low_stock)
@router.get("/products")   
def get_products(product_name: str = None, low_stock: bool = False):

    result = products_list

    if product_name:            
        result = [oneproduct for oneproduct in products_list if oneproduct.name.lower() == product_name.lower()]

    if low_stock:
        result = [secondproduct for secondproduct in result if secondproduct.quantity < 5]  # Note : I USED  "result"   list in searching   here VERY IMP
                                                                                            # Note: this will handle (both true or lowstock = true only)
                                                                                             # if both true , first it will filter from name , then from the filtered list it will filter the lowstock one only

    return result                                                                           # if both false , allready stored the intially one  so return it 



"""

OLD CODE :: dont write like this  , this is just for understanding the logic of the code and how to handle the query params in different cases


    if product_name == None and low_stock == False:
        return products_list
   
    elif product_name is not None and low_stock == True:
        pass
   
    elif product_name is not None:
        
        mathing_products=[]
        
        for oneproduct in products_list:
            if oneproduct.name.lower() == product_name.lower():
                mathing_products.append(oneproduct)
            
        return mathing_products
       
    else:
        
        low_stock_list = []
        
        for oneproduct in products_list:
            if oneproduct.quantity < 5:
                low_stock_list.append(oneproduct)
    
        return low_stock_list

"""




@router.get("/products/{product_id}")
def get_product(product_id : int):


    for oneproduct in products_list:
        if oneproduct.id == product_id:
            return oneproduct
        
    return {"message" : "Product not found"}





@router.put("/products/{given_product_id}")
def update_product(given_product_id : int , updated_product : Product):


    global activity_id_counter

    updatedaction = None
    resultstored = None


    old_quantity = None
    old_price = None
    old_name = None


    updated_quantity_change=0

    for oneproduct in products_list:
        if oneproduct.id == given_product_id:

              # store old values
            old_quantity = oneproduct.quantity
            old_price = oneproduct.price
            old_name = oneproduct.name

             # update
            oneproduct.name = updated_product.name
            oneproduct.price = updated_product.price
            oneproduct.quantity = updated_product.quantity

            resultstored = oneproduct



            """
                 resultstored = oneproduct

                oneproduct.name = updated_product.name
                oneproduct.price = updated_product.price
                oneproduct.quantity = updated_product.quantity

                finalresult = oneproduct
            """
            
            break

    if resultstored is None:
        return {"message" : "Product not found"}
    


    name_changed = updated_product.name != old_name
    price_changed = updated_product.price != old_price
    quantity_changed = updated_product.quantity != old_quantity


    if name_changed and price_changed and quantity_changed:
        updatedaction = "Name_Price_and_Quantity_Changed"
    
    elif price_changed and quantity_changed:
        updatedaction = "Price_and_Quantity_Changed"

    elif name_changed and price_changed:
        updatedaction = "Name_and_Price_Changed"

    elif name_changed and quantity_changed:
        updatedaction = "Name_and_Quantity_Changed"

    elif quantity_changed:
        if updated_product.quantity > old_quantity:
            updatedaction = "Quantity_Increased"
        else:
            updatedaction = "Quantity_Decreased"
    
    elif price_changed:
        updatedaction = "Price_Changed"

    elif name_changed:
        updatedaction = "Name_Changed_Only"  # if only name changed or any other details changed except price and quantity



    if updated_product.quantity != old_quantity:
        updated_quantity_change = updated_product.quantity - old_quantity

    if updatedaction is not None:
        latestactivity = Activity(
            id = activity_id_counter,
            product_id=given_product_id,
            action=updatedaction,
            quantity_change=updated_quantity_change

        )

        activity_id_counter+=1

        activities_list.append(latestactivity)

    return resultstored



    """
    

    
@router.put("/products/{given_product_id}")
def update_product(given_product_id : int , updated_product : Product):


    global activity_id_counter

    updatedaction = None

    resultstored = None
    finalresult = None

    updated_quantity_change=updated_product.quantity

    for oneproduct in products_list:
        if oneproduct.id == given_product_id:
                resultstored = oneproduct

                oneproduct.name = updated_product.name
                oneproduct.price = updated_product.price
                oneproduct.quantity = updated_product.quantity

                finalresult = oneproduct


            break

    if resultstored is None:
        return {"message" : "Product not found"}
    


    if updated_product.price != resultstored.price and updated_product.quantity != resultstored.quantity:  # seller changed both price and quantity
        updatedaction = "Price_and_Quantity_Changed"

    elif  updated_product.quantity > resultstored.quantity:  # seller increasing stock    
        updatedaction = "Quantity_Increased"
        
    elif updated_product.quantity < resultstored.quantity:# seller decreased stock  
        updatedaction = "Quantity_Decreased"
        
    elif updated_product.price != resultstored.price:  # seller price changed
        updatedaction = "Price_Changed"

    else:
        updatedaction = "Product_Details_Updated"  # if only name changed or any other details changed except price and quantity



    updated_quantity_change = updated_product.quantity - resultstored.quantity


    
    if updatedaction is not None:

        latestactivity = Activity(
            id = activity_id_counter,
            product_id=given_product_id,
            action=updatedaction,
            quantity_change=updated_quantity_change

        )

        activity_id_counter+=1

        activities_list.append(latestactivity)


    # for oneproduct in products_list:
    #     if oneproduct.id == given_product_id:
    #             oneproduct.name = updated_product.name
    #             oneproduct.price = updated_product.price
    #             oneproduct.quantity = updated_product.quantity
    #             break
        


    return finalresult



    """

    




@router.delete("/products/{given_id}")
def delete_product(given_id : int):


    global activity_id_counter
    deleted_product = None

    for oneproduct in products_list:
        if oneproduct.id == given_id:

            deleted_product = oneproduct



            latestactivity = Activity(
                id = activity_id_counter,
                product_id=given_id,
                action="DELETED",
                quantity_change=-oneproduct.quantity
            )

            activities_list.append(latestactivity)

            activity_id_counter+=1

            

            products_list.remove(oneproduct)
            return deleted_product

    return {"message" : "Product not found"}