# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database imports
from core.database import engine, Base

# Import all ORM models so metadata is populated
from db.models.professor import Professor
from db.models.guideline import Guideline
from db.models.question import Question
from db.models.student import Student
from db.models.test import Test
from db.models.student_answer import StudentAnswer

# Routers
from routers.prueba import router as prueba_router
from routers.files import router as files_router
from routers.analyze import router as analyze_router
from routers.parse_ocr import router as parse_ocr_router
from routers.save_file import router as save_file_router
from routers.save_test import router as save_test_router
from routers.tests import router as tests_router
from routers.students import router as students_router
from routers.students_answers import router as students_answers_router
from routers.questions import router as questions_router
from routers.prompting import router as prompting_router
from routers.guidelines import router as guidelines_router
from routers.professors import router as professors_router

# FastAPI app instance
app = FastAPI(
    title="My FastAPI Project",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers under /api/v1
prefix = "/api/v1"
app.include_router(prueba_router, prefix=prefix)
app.include_router(files_router, prefix=prefix)
app.include_router(analyze_router, prefix=prefix)
app.include_router(parse_ocr_router, prefix=prefix)
app.include_router(save_file_router, prefix=prefix)
app.include_router(save_test_router, prefix=prefix)
app.include_router(tests_router, prefix=prefix)
app.include_router(students_router, prefix=prefix)
app.include_router(students_answers_router, prefix=prefix)
app.include_router(questions_router, prefix=prefix)
app.include_router(prompting_router, prefix=prefix)
app.include_router(guidelines_router, prefix=prefix)
app.include_router(professors_router, prefix=prefix)

# Create tables on startup
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Home Page"}
