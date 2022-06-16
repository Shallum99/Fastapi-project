from fastapi import FastAPI

import models
from database import engine
from routers import doctors, patients, nurses, admin, records, auth


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(doctors.router)
app.include_router(patients.router)
app.include_router(nurses.router)
app.include_router(admin.router)
app.include_router(records.router)
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"Hello": "This is healthamanagement api"}


