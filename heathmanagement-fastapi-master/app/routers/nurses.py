from fastapi import Response, status, HTTPException, Depends, APIRouter

from sqlalchemy.orm import Session

from database import get_db
from schemas import Nurse
import models


router = APIRouter( prefix="/nurse", tags=["Nurse"])

@router.get("")
def get_nurse(db: Session = Depends(get_db)):
    """
    Returns the list of all nurses
    """
    nurse_query = db.query(models.Nurse)

    nurse = nurse_query.all()

    return nurse


@router.get("/{nurse_id}")
def get_nurse(nurse_id: int, db: Session = Depends(get_db)):
    """
    Returns the list of nurse by id
    """
    
    nurse_query = db.query(models.Nurse).filter(models.Nurse.nurse_id == nurse_id)
    
    nurse = nurse_query.first()

    if nurse == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"nurse with id: {nurse_id} does not exist")
    
    return nurse


@router.post("", status_code=status.HTTP_201_CREATED)
def post_nurse(nurse:Nurse, db: Session = Depends(get_db)):
    """
    To add the nurse in the database by post request
    """
    new_nurse = models.Nurse(**nurse.dict())

    if nurse == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials")
    
    db.add(new_nurse)
    db.commit()
    db.refresh(new_nurse)

    return new_nurse


@router.put("/{id}")
def update_nurse(id: int, updated_post: Nurse, db: Session = Depends(get_db)):
    """
    To update the nurse in the database by id
    """

    update_query = db.query(models.Nurse).filter(models.Nurse.nurse_id == id)

    update = update_query.first()

    if update == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"nurse with id: {id} does not exist")

    update_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return update_query.first()


@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
    """
    To delete the nurse in the database by id
    """

    delete_query = db.query(models.Nurse).filter(models.Nurse.nurse_id == id)

    delete = delete_query.first()

    if delete == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"nurse with id: {id} does not exist")

    delete_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)