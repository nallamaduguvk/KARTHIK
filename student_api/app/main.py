import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from typing import List

from .models import StudentCreate, Student
from .repository import (
    StudentRepository,
    InMemoryStudentRepository,
    MongoStudentRepository,
)

app = FastAPI(title="Student API")
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

# Dependency to get repository
def get_repository() -> StudentRepository:
    uri = os.getenv("MONGODB_URI")
    if uri:
        db_name = os.getenv("MONGODB_DB", "studentdb")
        return MongoStudentRepository(uri, db_name)
    return InMemoryStudentRepository()

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/students", response_model=Student, status_code=201)
async def create_student(student: StudentCreate, repo: StudentRepository = Depends(get_repository)) -> Student:
    return await repo.create(student)

@app.get("/students", response_model=List[Student])
async def list_students(repo: StudentRepository = Depends(get_repository)) -> List[Student]:
    return await repo.list()

@app.get("/students/{student_id}", response_model=Student)
async def get_student(student_id: str, repo: StudentRepository = Depends(get_repository)) -> Student:
    student = await repo.get(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.put("/students/{student_id}", response_model=Student)
async def update_student(student_id: str, student_data: StudentCreate, repo: StudentRepository = Depends(get_repository)) -> Student:
    updated = await repo.update(student_id, student_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Student not found")
    return updated

@app.delete("/students/{student_id}", status_code=204)
async def delete_student(student_id: str, repo: StudentRepository = Depends(get_repository)) -> None:
    success = await repo.delete(student_id)
    if not success:
        raise HTTPException(status_code=404, detail="Student not found")
    return None
