from abc import ABC, abstractmethod
from typing import List, Optional
from .models import StudentCreate, Student

class StudentRepository(ABC):
    @abstractmethod
    async def create(self, student: StudentCreate) -> Student:
        pass

    @abstractmethod
    async def list(self) -> List[Student]:
        pass

    @abstractmethod
    async def get(self, student_id: str) -> Optional[Student]:
        pass

    @abstractmethod
    async def update(self, student_id: str, student: StudentCreate) -> Optional[Student]:
        pass

    @abstractmethod
    async def delete(self, student_id: str) -> bool:
        pass

class InMemoryStudentRepository(StudentRepository):
    def __init__(self) -> None:
        self.students = {}
        self.current_id = 0

    async def create(self, student: StudentCreate) -> Student:
        self.current_id += 1
        new = Student(id=str(self.current_id), **student.dict())
        self.students[new.id] = new
        return new

    async def list(self) -> List[Student]:
        return list(self.students.values())

    async def get(self, student_id: str) -> Optional[Student]:
        return self.students.get(student_id)

    async def update(self, student_id: str, student: StudentCreate) -> Optional[Student]:
        if student_id not in self.students:
            return None
        updated = Student(id=student_id, **student.dict())
        self.students[student_id] = updated
        return updated

    async def delete(self, student_id: str) -> bool:
        if student_id in self.students:
            del self.students[student_id]
            return True
        return False

try:
    from motor.motor_asyncio import AsyncIOMotorClient
    from bson import ObjectId
except Exception:  # pragma: no cover - motor not installed in tests
    AsyncIOMotorClient = None  # type: ignore
    ObjectId = None  # type: ignore

class MongoStudentRepository(StudentRepository):
    def __init__(self, uri: str, db_name: str = "studentdb") -> None:
        if AsyncIOMotorClient is None:
            raise RuntimeError("motor is required for MongoStudentRepository")
        self.client = AsyncIOMotorClient(uri)
        self.collection = self.client[db_name]["students"]

    async def create(self, student: StudentCreate) -> Student:
        result = await self.collection.insert_one(student.dict())
        doc = await self.collection.find_one({"_id": result.inserted_id})
        return Student(id=str(doc["_id"]), **{k: doc[k] for k in student.dict().keys()})

    async def list(self) -> List[Student]:
        students = []
        async for doc in self.collection.find():
            students.append(Student(id=str(doc["_id"]), **{k: doc[k] for k in StudentCreate.__fields__.keys()}))
        return students

    async def get(self, student_id: str) -> Optional[Student]:
        if ObjectId is None:
            return None
        doc = await self.collection.find_one({"_id": ObjectId(student_id)})
        if doc:
            return Student(id=str(doc["_id"]), **{k: doc[k] for k in StudentCreate.__fields__.keys()})
        return None

    async def update(self, student_id: str, student: StudentCreate) -> Optional[Student]:
        if ObjectId is None:
            return None
        oid = ObjectId(student_id)
        result = await self.collection.replace_one({"_id": oid}, student.dict())
        if result.modified_count:
            return Student(id=student_id, **student.dict())
        return None

    async def delete(self, student_id: str) -> bool:
        if ObjectId is None:
            return False
        result = await self.collection.delete_one({"_id": ObjectId(student_id)})
        return result.deleted_count > 0
