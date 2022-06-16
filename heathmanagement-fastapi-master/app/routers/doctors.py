from fastapi import Response, status, HTTPException, Depends, APIRouter

from sqlalchemy.orm import Session

from database import get_db
from schemas import Doctor
import models


router = APIRouter( prefix="/doctor", tags=["Doctor"])

@router.get("")
def get_doctors(db: Session = Depends(get_db)):
    """
    Returns the list of all doctors
    """

    doctors= db.query(models.Doctor).all()

    if not doctors:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid credential")

    return doctors


@router.get("/{doc_id}")
def get_doctor(doc_id: int, db: Session = Depends(get_db)):
    """
    Returns the list of doctor by id
    """

    doctor = db.query(models.Doctor).filter(models.Doctor.doctor_id == doc_id).first()

    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Doctor with id: {id} was not found")

    return doctor


@router.post("", status_code=status.HTTP_201_CREATED)
def post_doctor(doctor:Doctor, db: Session = Depends(get_db)):
    """
    To add the doctor in the database by post request
    """

    new_doc = models.Doctor(**doctor.dict())

    if not new_doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Doctor with id: {id} was not found")

    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)

    return new_doc


@router.put("/{id}")
def update_doctor(id: int, updated_post: Doctor, db: Session = Depends(get_db)):
    """
    To update the doctor by id
    """

    update_query = db.query(models.Doctor).filter(models.Doctor.doctor_id == id)

    post = update_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Doctor with id: {id} does not exist")

    update_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return update_query.first()


@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
    """
    To delete the doctor by id
    """

    delete_query = db.query(models.Doctor).filter(models.Doctor.doctor_id == id)

    post = delete_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Doctor with id: {id} does not exist")

    delete_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)