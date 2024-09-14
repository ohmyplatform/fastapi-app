import os
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# Leer la URL de la base de datos desde la variable de entorno
DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("La variable de entorno DATABASE_URL no está configurada.")

# Crear el motor de conexión
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Definir el modelo Course
class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    description = Column(String(255))

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Modelos Pydantic
class CourseBase(BaseModel):
    name: str
    description: str

class CourseCreate(CourseBase):
    pass

class CourseOut(CourseBase):
    id: int

    class Config:
        orm_mode = True

# Crear la aplicación FastAPI
app = FastAPI()

# Dependencia para obtener la sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoints de la API
@app.get("/courses", response_model=list[CourseOut])
def read_courses(skip: int = 0, limit: int = 100, db=Depends(get_db)):
    courses = db.query(Course).offset(skip).limit(limit).all()
    return courses

@app.get("/courses/{course_id}", response_model=CourseOut)
def read_course(course_id: int, db=Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if course is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return course

@app.post("/courses", response_model=CourseOut)
def create_course(course: CourseCreate, db=Depends(get_db)):
    db_course = Course(name=course.name, description=course.description)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

@app.get("/health/live", include_in_schema=False)
def liveness():
    return {"status": "alive"}

@app.get("/health/ready", include_in_schema=False)
def readiness(db=Depends(get_db)):
    try:
        # Realizar una consulta simple para verificar la conexión a la base de datos
        db.execute("SELECT 1")
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Error en la conexión a la base de datos")
    return {"status": "ready"}