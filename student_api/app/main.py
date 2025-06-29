from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field
from typing import Dict, List

app = FastAPI(title="Student API")

class StudentBase(BaseModel):
    first_name: str = Field(..., example="John")
    last_name: str = Field(..., example="Doe")
    grade: str = Field(..., example="10")
    age: int = Field(..., ge=1, example=15)
    phone_number: str = Field(..., example="1234567890")
    email: EmailStr = Field(..., example="john@example.com")
    address: str = Field(..., example="123 Main St")
    father_name: str = Field(..., example="Father Name")
    mother_name: str = Field(..., example="Mother Name")

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int

# In-memory store
students: Dict[int, Student] = {}
current_id: int = 0

@app.post("/students", response_model=Student, status_code=201)
def create_student(student: StudentCreate) -> Student:
    global current_id
    current_id += 1
    new_student = Student(id=current_id, **student.dict())
    students[current_id] = new_student
    return new_student

@app.get("/students", response_model=List[Student])
def list_students() -> List[Student]:
    return list(students.values())

@app.get("/students/{student_id}", response_model=Student)
def get_student(student_id: int) -> Student:
    student = students.get(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.put("/students/{student_id}", response_model=Student)
def update_student(student_id: int, student_data: StudentCreate) -> Student:
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    updated = Student(id=student_id, **student_data.dict())
    students[student_id] = updated
    return updated

@app.delete("/students/{student_id}", status_code=204)
def delete_student(student_id: int) -> None:
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    del students[student_id]
    return None
