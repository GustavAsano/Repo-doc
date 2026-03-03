from pydantic import BaseModel, Field


# Define default error response
class ErrorResponse(BaseModel):
    error: str = Field(..., description="The error message")
