from fastapi import Response, status, HTTPException, Depends, APIRouter

from sqlalchemy.orm import Session

from database import get_db
from schemas import Patient
import models


router = APIRouter( prefix="/patient", tags=["Patient"])

@router.get("")
def get_patient(db: Session = Depends(get_db)):
    """
    Returns the list of all patients
    """

    patient_query = db.query(models.Patient)

    patient = patient_query.all()

    return patient


@router.get("/{patient_id}")
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    """
    Returns the list of patients by id
    """
    
    patient_query = db.query(models.Patient).filter(models.Patient.patient_id == patient_id)
    
    patient = patient_query.first()

    if patient == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"patient with id: {patient_id} does not exist")
    
    return patient


@router.post("", status_code=status.HTTP_201_CREATED)
def post_patient(patient:Patient, db: Session = Depends(get_db)):
    """
    To add the patient in the database by post request
    """

    new_patient = models.Patient(**patient.dict())

    if patient == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials")
    
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    return new_patient


@router.put("/{id}")
def update_patient(id: int, updated_post: Patient, db: Session = Depends(get_db)):
    """
    To update the patient in the database by id
    """

    update_query = db.query(models.Patient).filter(models.Patient.patient_id == id)

    update = update_query.first()

    if update == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"patient with id: {id} does not exist")

    update_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return update_query.first()


@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
    """
    To delete the patient in the database by id
    """

    delete_query = db.query(models.Patient).filter(models.Patient.patient_id == id)

    delete = delete_query.first()

    if delete == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"patient with id: {id} does not exist")

    delete_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)