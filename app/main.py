from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from app.database import engine, Base
from app.core.errors import AppError, ErrorResponse
from app.alerts.router import router as alerts_router

# Create database tables if they do not exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Captain Hawkeye API")

# Configure CORS middleware (dev-only MVP setting: allow all origins, methods, headers)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=True,
            message=exc.message,
            status_code=exc.status_code
        ).model_dump()
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # ASSUMPTION: Convert Pydantic/FastAPI validation errors into standard ErrorResponse shape with 400 status code
    return JSONResponse(
        status_code=400,
        content=ErrorResponse(
            error=True,
            message=str(exc),
            status_code=400
        ).model_dump()
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error=True,
            message="Internal Server Error",
            status_code=500
        ).model_dump()
    )

# Root endpoint - redirect to interactive documentation
@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


# Include alert router
app.include_router(alerts_router)

# TODO: Dev 1 will include app.anpr.router here later
# app.include_router(anpr.router)

# TODO: Dev 2 will include app.trajectory.router here later
# app.include_router(trajectory.router)

