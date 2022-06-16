from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List

from sqlalchemy.orm import Session

from database import get_db
from schemas import Record, RecordPost
import oauth2
import models


router = APIRouter( prefix="/record", tags=["Records"])

@router.get("", response_model=List[RecordPost])
def get_record(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    """
    Returns the list of all records 
    """
    
    record_query = db.query(models.Record)

    record = record_query.all()

    return record


@router.get("/{record_id}", response_model=RecordPost)
def get_record(record_id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    """
    Returns the list of records by id
    """

    record_query = db.query(models.Record).filter(models.Record.record_id == record_id)
    
    record = record_query.first()

    if record == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"record with id: {record_id} does not exist")
    
    return record


@router.post("", status_code=status.HTTP_201_CREATED, response_model=RecordPost)
def post_record(record:Record, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    """
    To add the record in the database by post request
    """

    new_record = models.Record(**record.dict())

    if record == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials")
    
    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return new_record


@router.put("/{id}", response_model=RecordPost)
def update_record(id: int, updated_post: Record, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    """
    To update the record in the database by id
    """

    update_query = db.query(models.Record).filter(models.Record.record_id == id)

    update = update_query.first()

    if update == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"record with id: {id} does not exist")

    update_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return update_query.first()


@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    """
    To delete the patient in the database by id
    """

    delete_query = db.query(models.Record).filter(models.Record.record_id == id)

    delete = delete_query.first()

    if delete == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"record with id: {id} does not exist")

    delete_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)