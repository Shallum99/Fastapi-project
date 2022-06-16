from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr


class Doctor(BaseModel):
    """
    Schema for the Doctor model.
    """

    doctor_id: int
    doctor_name: str
    doctor_dept: str
    doctor_adhar: str
    doctor_address: str
    doctor_mobile: int
    patient_id: int


class Patient(BaseModel):
    """
    Schema for the patient model.
    """

    patient_id: int
    patient_name: str
    patient_adhar: str
    patient_address: str
    patient_mobile: int

    class Config:
        orm_mode = True


class Record(BaseModel):
    """
    Schema for the Record model.
    """

    record_id: int
    doctor_name: str
    issue: str
    patient_id: int
    doctor_id: int
    admin_id: int
    appointment_date: date

    class Config:
        orm_mode = True


class Nurse(BaseModel):
    """
    Schema for the Nurse model.
    """

    nurse_id: int
    nurse_name: str
    nurse_adhar: str
    nurse_address: str
    nurse_mobile: int
    doctor_id: int

    class Config:
        orm_mode = True

class Admin(BaseModel):
    """
    Schema for the Admin model.
    """

    admin_id: int
    admin_name: str
    admin_pass: str
    admin_email: EmailStr
    bed_avail: int
    doc_avail: int
    nurse_avail: int

    class Config:
        orm_mode = True


class RecordPost(Record):
    """
    Response Schema for the Doctor model.
    """

    owner: Admin

    class Config:
        orm_mode = True


class AdminLogin(BaseModel):
    """
    Response Schema for the Doctor model.
    """

    admin_email: EmailStr
    admin_pass: str


class Token(BaseModel):
    """
    Schema for the Token.
    """
    
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Response Schema for the token data.
    """

    id: Optional[str] = None