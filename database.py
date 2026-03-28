#step1 : the imports

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base



#step2 : The URL: Define that "Address" string we talked about: sqlite:///./inventory.db.

SQLALCHEMY_DATABASE_URL = "sqlite:///./inventory.db"   # Database Connection URL



# Step3

engine = create_engine(
    SQLALCHEMY_DATABASE_URL , connect_args={"check_same_thread" : False}   # this is for sqlite db , for other db we dont need this
)

                                                                        # Because SQLite is a file, it usually only allows one "thread" to talk to it at a time. 

                                                                        # But FastAPI is asynchronous and multi-threaded. 
                                                                        # We add connect_args={"check_same_thread": False}




#step4 : create a session local class which will be used to create db sessions in our api endpoints  and also in the future for any db operations like : create , read , update , delete  (CRUD) operations 

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# step5 : create a base class for our models to inherit from it
# Step 5: The Base Class
# Finally, we create the Base. Later, in your models.py, your Product and Order classes will "inherit" from this. This is how SQLAlchemy knows: "Aha! These Python classes are actually Database Tables."

Base = declarative_base()




# read the explntion below written what it is , why need , what if we not write(issues we got if not written)
# # This function is a "generator"
def get_db():
    db = SessionLocal() # 1. Open the session
    try:
        yield db        # 2. Give the session to the route
    finally:
        db.close()      # 3. Always close it when finished




"""

basically : 

first create a session( connection , to inventory.db file // open a connect)
second : yield(pause) so that we can add the product or whatever sent route work
third : after the route work is done , close the connection to the file (release the memory)



In your product.py, when a seller calls @router.post("/products"), FastAPI doesn't just run your code. It sees Depends(get_db) and follows this exact sequence:

db = SessionLocal(): The computer carves out a small piece of RAM (memory) specifically to talk to inventory.db. This is your "active connection."

yield db: The computer pauses the get_db function right here. It "hands" that piece of memory (db) to your add_product function so you can run db.add(new_item).

The "Wait": Your add_product code finishes running and returns the new product to the seller.

finally: db.close(): Now that your route is done, the computer "wakes up" the get_db function and runs the last line. It releases that RAM and cuts the connection to the file.

"""



"""

If you don't write the get_db() function, you would have to manually open and close the database connection inside every single route (Add Product, Update Product, Delete Product, etc.).

Without get_db(), your code in product.py would look like this (The "Bad" Way):

Python
@router.post("/products")
def add_product(oneproduct: ProductSchema):
    db = SessionLocal()  # Manually open
    
    # ... your logic here ...
    
    db.add(new_item)
    db.commit()
    
    db.close()           # Manually close (BUT what if the code crashes before this line?)
    return oneproduct


The 3 Risks of skipping get_db():

1. The "Database is Locked" Error (Most Common)
In your update_product logic, you have a lot of if/else checks. If your code hits a return statement or an error before it reaches db.close(), that connection stays "hanging."
Because SQLite is just a single file on your Windows disk, it can only handle so many open "handles." Eventually, when you try to GET /products, SQLite will throw an error: "database is locked" because the previous PUT request never let go of the file.

2. Code Repetition (DRY Principle)
You have about 5-6 routes in product.py and more in customer.py. Without get_db(), you would have to write db = SessionLocal() and db.close() in every single one. If you decide to change how your sessions work later, you’d have to fix it in 10 different places.

With get_db(), you define the logic once and just "inject" it into your routes.

3. Handling Crashes
If a seller sends a "String" instead of an "Integer" for price, and your logic crashes, a manual db.close() at the bottom of the function will never run.
The get_db() function uses finally:, which is a guarantee in Python. It tells the computer: "I don't care if the code crashed, succeeded, or exploded—run the close command no matter what."


🚀 Summary
get_db() is like an Automated Door Closer.

Without it: You have to remember to lock the door every time you leave. If you forget once, the house is at risk.

With it: The door has a spring. It closes itself the moment you walk out.


"""