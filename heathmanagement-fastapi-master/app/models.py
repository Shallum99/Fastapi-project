from sqlalchemy import (
     BigInteger, 
     Column, 
     Integer, 
     String, 
     ForeignKey,
     Date,
)
from sqlalchemy_utils import EmailType
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types.choice import ChoiceType

from database import Base


class Doctor(Base):
    """
    Model for Doctors in healthmanagement.
    """

    departments=[('Cardiologist','Cardiologist'),
                 ('Dermatologists','Dermatologists'),
                 ('Emergency Medicine Specialists','Emergency Medicine Specialists'),
                 ('Allergists/Immunologists','Allergists/Immunologists'),
                 ('Anesthesiologists','Anesthesiologists'),
                 ('Colon and Rectal Surgeons','Colon and Rectal Surgeons')
    ]
    
    __tablename__ = "doctors"

    doctor_id = Column(Integer, primary_key=True, nullable=False)
    doctor_name = Column(String, nullable=False)
    doctor_dept = Column(ChoiceType(departments))
    doctor_adhar = Column(String(12), nullable=False)
    doctor_address = Column(String, nullable = False)
    doctor_mobile = Column(BigInteger, nullable = False)
    patient_id = Column(Integer, ForeignKey(
        "patients.patient_id", ondelete="CASCADE"))


class Admin(Base):
    """
    Model for Admins in healthmanagement.
    """

    __tablename__ = "admin"

    admin_id = Column(Integer, primary_key=True, nullable=False)
    admin_name = Column(String, nullable=False)
    admin_pass = Column(String, nullable=False)
    admin_email = Column(EmailType, nullable = False)
    bed_avail = Column(Integer, nullable=False)
    doc_avail = Column(Integer, nullable=False)
    nurse_avail = Column(Integer, nullable=False)


class Patient(Base):
    """
    Model for Patients in healthmanagement.
    """

    __tablename__ = "patients"

    patient_id = Column(Integer, primary_key=True, nullable=False)
    patient_name = Column(String, nullable=False)
    patient_adhar = Column(String(12), nullable=False)
    patient_address = Column(String, nullable = False)
    patient_mobile = Column(BigInteger, nullable = False)   


class Record(Base):
    """
    Model for Records in healthmanagement.
    """
    #Encounter
    __tablename__ = "records"

    record_id = Column(Integer, primary_key=True, nullable=False)
    doctor_name = Column(String, nullable=False)
    issue = Column(String, nullable=False)
    patient_id =  patient_id = Column(Integer, ForeignKey(
        "patients.patient_id", ondelete="CASCADE"))
    doctor_id = Column(Integer, ForeignKey(
        "doctors.doctor_id", ondelete="CASCADE"))
    admin_id = Column(Integer, ForeignKey(
        "admin.admin_id", ondelete="CASCADE"))
    appointment_date = Column(Date, nullable=False)
    owner = relationship("Admin")


class Nurse(Base):
    """
    Model for Nurses in healthmanagement.
    """

    __tablename__ = "nurses"

    nurse_id = Column(Integer, primary_key=True, nullable=False)
    nurse_name = Column(String, nullable=False)
    nurse_adhar = Column(String(12), nullable=False)
    nurse_address = Column(String, nullable = False)
    nurse_mobile = Column(BigInteger, nullable = False)
    doctor_id = Column(Integer, ForeignKey(
        "doctors.doctor_id", ondelete="CASCADE"))


#Feedback
#dont use repetitive prefix
#patient model foreign key
#id generation at backend
#alembic
#unit test cases and integration - main
#linter - black
#precommit githooks