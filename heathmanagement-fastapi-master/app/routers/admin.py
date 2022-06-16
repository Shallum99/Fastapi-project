from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List

from sqlalchemy.orm import Session

from database import get_db
from schemas import Admin
import models
import utils


router = APIRouter( prefix="/admin", tags=["Admin"])

@router.get("")
def get_admin(db: Session = Depends(get_db)):
    """
    Returns the list of all admins
    """

    admin_query = db.query(models.Admin)

    admin = admin_query.all()

    return admin


@router.get("/{admin_id}")
def get_admin(admin_id: int, db: Session = Depends(get_db)):
    """
    Returns the list of admin by id
    """
    
    admin_query = db.query(models.Admin).filter(models.Admin.admin_id == admin_id)
    
    admin = admin_query.first()

    if admin == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Admin with id: {admin_id} does not exist")
    
    return admin


@router.post("", status_code=status.HTTP_201_CREATED)
def post_admin(admin:Admin, db: Session=Depends(get_db)):
    """
    To add the admin in the database by post request
    """

    hashed_password = utils.hash(admin.admin_pass)
    admin.admin_pass = hashed_password

    new_admin = models.Admin(**admin.dict())

    if admin == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials")
    
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    return new_admin


@router.put("/{id}")
def update_admin(id: int, updated_post: Admin, db: Session=Depends(get_db)):
    """
    To update the admin by id
    """

    update_query = db.query(models.Admin).filter(models.Admin.admin_id == id)

    update = update_query.first()

    if update == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"admin with id: {id} does not exist")

    update_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return update_query.first()


@router.delete("/{id}")
def delete_post(id: int, db: Session=Depends(get_db)):
    """
    To delete the admin by id
    """

    delete_query = db.query(models.Admin).filter(models.Admin.admin_id == id)

    delete = delete_query.first()

    if delete == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"admin with id: {id} does not exist")

    delete_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)