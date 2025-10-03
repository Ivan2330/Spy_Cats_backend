from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

def install_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(ValidationError)
    async def pydantic_error_handler(request: Request, exc: ValidationError):
        return JSONResponse(status_code=422, content={"detail": exc.errors()})
