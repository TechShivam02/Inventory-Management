from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas





router = APIRouter()



@router.post("/products")
def add_product(oneproduct : schemas.ProductCreate , db:Session = Depends(get_db)):
    # 1. Convert Pydantic to SQLAlchemy model

    #note : we can't use oneprduct directly to add in the database because it is a pydantic model and we need to convert it to a sqlalchemy model to add in the database
    latestoneproduct = models.Product(
        name = oneproduct.name,
        price = oneproduct.price,
        quantity = oneproduct.quantity
    )

    

# 2. Add and COMMIT to generate the ID
    db.add(latestoneproduct)
    db.commit()    # If you don't commit the product immediately, the database hasn't assigned it an ID yet. In Python, latestoneproduct.id is still None.
    db.refresh(latestoneproduct)   # here we refersh , bcz we need the id of  "latestoneproduct" in the activity in the same block

    

# 3. Use that ID for the Activity
    latestactivity = models.Activity(
        product_id=latestoneproduct.id,    # here wew using 
        action="CREATED",
        quantity_change=latestoneproduct.quantity
    )


    db.add(latestactivity)
    db.commit()
    # db.refresh(latestactivity)   # no need to refersh activity because we are not using the id of activity anywhere in the code , but if we want to use it then we can refresh it here
    



    return latestoneproduct











                            # VERY IMP :: get all the products   // LIKE the FILTER one (if have to get by product name  and low_stock)
@router.get("/products")   
def get_products(product_name: str = None, low_stock: bool = False , db:Session = Depends(get_db)):

                                        
    query = db.query(models.Product) # 1. Start a basic query for all products



    
    if low_stock:
        query = query.filter(models.Product.quantity < 5)  # 2 : If the user checked "low_stock", add another filter
                # vimp : NOT ,, db.query.filter(models.Product.quantity < 5)
                # ython got confused because db.query is a tool that needs to know what to look for (like models.Product) every time you call it. 

    if product_name:     # very imp : why not used .lower()  as used earlier (EXPLNATION : written below  ( bcz of INDEXING , SLOW ))
        query = query.filter(models.Product.name.ilike(f"%{product_name}%"))  # 3  .filter() is like your "if name == product_name"
                #  vimp : NOT ,, db.query.filter(models.Product.name.iLike(f"%{product_name}%"))   # this will not work because db.query is a tool that needs to know what to look for (like models.Product) every time you call it. If you write db.query.filter() without specifying the model, Python gets confused about what you're trying to filter. You need to specify the model (like models.Product) so that Python knows which table's name column you're referring to when you call .filter().
                #  now , case insensitve , both and only the same char if present   will also work


    products = query.all() # 4 Finally, execute the query and get the list

    return products

""""

While name.lower() == product_name.lower() works in pure Python lists, it behaves differently when talking to a database (SQL). Here is the breakdown of why we use .ilike() instead of .lower():

1. The "Database vs. Python" Problem
When you write models.Product.name.lower(), SQLAlchemy tries to translate that into a SQL command.

1.1)Some databases (like SQLite) handle .lower() okay, but others (like PostgreSQL) can be very slow when you do this because they have to transform every single row before checking the name.

1.2)The "Index" Issue: Databases use an "Index" (like the index at the back of a book) to find NAMES instantly. If you use .lower(), the database often can't use its index, 


2. The Power of .ilike()

The .ilike() (Insenstive Like) is a built-in SQL power tool. It does exactly what you want: Case-Insensitive matching.

Code	What it finds for "iPhone"	Logic
.filter(models.Product.name == product_name)	"iPhone" only	Exact match.
.filter(models.Product.name.ilike(product_name))	"iphone", "IPHONE", "iPhone"	Case-insensitive.
.filter(models.Product.name.ilike(f"%{product_name}%"))	"iPhone 15", "Old iPhone", "iphone"	Contains the word + Case-insensitive.


"""


    # result = products_list

    # if product_name:            
    #     result = [oneproduct for oneproduct in products_list if oneproduct.name.lower() == product_name.lower()]

    # if low_stock:
    #     result = [secondproduct for secondproduct in result if secondproduct.quantity < 5]  # Note : I USED  "result"   list in searching   here VERY IMP
    #                                                                                         # Note: this will handle (both true or lowstock = true only)
    #                                                                                          # if both true , first it will filter from name , then from the filtered list it will filter the lowstock one only

    # return result                                                                           # if both false , allready stored the intially one  so return it 



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
def get_product(product_id : int , db:Session = Depends(get_db)):


    result = db.query(models.Product).get(product_id)

        # second way : db.query(models.Product).filter(models.Product.id == product_id).first()   # this is also same as above one but above one is more efficient because it uses primary key to get the product directly , but this one will search through all the products and then return the matching one

    if (result is None):
        return {"message": "Product not found"}
    
    return result



"""
second way , a little more to add , without .first()  one 


Code                                What result becomes                         Can you do result.name?

db.query(...).filter(...)	        A Query Instruction	                        No (It's not data yet)
db.query(...).filter(...).all()	    A List of objects: [all products]	        No (You'd need result[0].name)
db.query(...).filter(...).first()	The Actual Object: Product	                Yes!



"""








@router.put("/products/{given_product_id}")                 # Note : product will come from pydantic model and we need to convert it to sqlalchemy model to update in the database , not directly use the from the model one (parameter)
def update_product(given_product_id : int , updated_product : schemas.ProductCreate , db:Session = Depends(get_db)):
    
    # 1. Fetch the live object
    
    oneproduct = db.query(models.Product).get(given_product_id)

    if oneproduct is None:
        return {"message" : "Product not found"}
    
        # store old values
    # 2. Store old values for the log

    old_quantity = oneproduct.quantity
    old_price = oneproduct.price    
    old_name = oneproduct.name


    # 3. Update the live object (SQLAlchemy tracks these changes)
    # update
    oneproduct.name = updated_product.name
    oneproduct.price = updated_product.price
    oneproduct.quantity = updated_product.quantity

                    # very imp below one
    # db.commit()   // no need to commit here at last we do comit at once after the activity change also 
                   # Problem : d db.commit() after updating the product, and then another db.commit() after the activity. This is okay, but if the second commit fails, your product is updated while your log is missing.
    # db.refresh(oneproduct)  // at the end we can refresh the oneproduct to get the updated values after commit and then return it , but if we do it here before commit then it will not give us the updated values because we have not commited the changes to the database yet , so we can do it at the end after commit and before return statement


    updatedaction = None


    # 4. Calculate your Activity Log (your logic is perfect here)

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


    # 5. Add the activity IF something changed
    if updatedaction is not None:

        latestactivity = models.Activity(

            product_id=given_product_id,
            action=updatedaction,
            quantity_change=updated_product.quantity - old_quantity

        )

        db.add(latestactivity)



# 6. COMMIT ONCE! This saves the product changes AND the activity at the same time.

        db.commit()
        db.refresh(oneproduct)   # to get the updated values of oneproduct after commit



    return oneproduct








"""


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



            
                # resultstored = oneproduct

                # oneproduct.name = updated_product.name
                # oneproduct.price = updated_product.price
                # oneproduct.quantity = updated_product.quantity

                # finalresult = oneproduct
        
            
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
    






    



@router.delete("/products/{given_id}")
def delete_product(given_id : int , db:Session = Depends(get_db)):

    product = db.query(models.Product).get(given_id)

    if product is None:
        return {"message" : "Product not found"}
    
    latestactivity = models.Activity(
        product_id = given_id,
        action="DELETED",
        quantity_change=-product.quantity
    )

    db.add(latestactivity)
    # db.commit()

    db.delete(product)  # NOTE : db.query(models.Product).delete(resultqueryFound)   # this will not work because delete() method is used to delete the whole table or delete based on filter condition , but we have already found the product using get() method so we can directly use db.delete() method to delete that specific product
    db.commit()

    return {
        "message" : "Product deleted successfully"
    }




    # global activity_id_counter
    # deleted_product = None

    # for oneproduct in products_list:
    #     if oneproduct.id == given_id:

    #         deleted_product = oneproduct



    #         latestactivity = Activity(
    #             id = activity_id_counter,
    #             product_id=given_id,
    #             action="DELETED",
    #             quantity_change=-oneproduct.quantity
    #         )

    #         activities_list.append(latestactivity)

    #         activity_id_counter+=1

            

    #         products_list.remove(oneproduct)
    #         return deleted_product

    # return {"message" : "Product not found"}