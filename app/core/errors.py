from pydantic import BaseModel

class AppError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

class ErrorResponse(BaseModel):
    error: bool = True
    message: str
    status_code: int
