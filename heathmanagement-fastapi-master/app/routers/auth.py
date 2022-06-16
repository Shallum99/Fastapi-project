from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

import utils
import oauth2
import models
import database


router = APIRouter(prefix="/login", tags=["Authorization"])

@router.post("", status_code=status.HTTP_201_CREATED)
def user_login(user_cred: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    """
    Returns the access token to acces the patient records
    """

    user = db.query(models.Admin).filter(
        models.Admin.admin_email == user_cred.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    if not utils.verify(user_cred.password, user.admin_pass):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    access_token = oauth2.create_access_token(data={"user_id": user.admin_id})

    return {"access_token": access_token, "token_type": "bearer"}