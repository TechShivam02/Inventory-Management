from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models



router = APIRouter()

@router.get("/activities")
def getactivities(db:Session = Depends(get_db)):
    # activities = db.query(models.Activity).all()  // to get all activities

    activities = db.query(models.Activity).order_by(models.Activity.id.desc()).all()
                            # order_by(models.Activity.id.desc()) : will arange the new activt to old activ -> from top to bottom
    return activities



@router.get("/activities/{product_id}")
def getactivity(product_id : int , db:Session=Depends(get_db)):


    Allactivities = db.query(models.Activity).filter(models.Activity.product_id == product_id).all()

    if not Allactivities:
        return {"message" : "Product not found"}
    
    return Allactivities
    

