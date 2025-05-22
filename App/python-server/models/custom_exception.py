from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import Request
from fastapi.exception_handlers import request_validation_exception_handler

# Customized handler for RequestValidationError errors
async def custom_validation_exception_handler(request: Request, exc: RequestValidationError):
    status_code = 422
    if exc.errors():
        error_detail = exc.errors()[0]
        # Extracting the first error detail
        loc_list = error_detail.get("loc", [])
        str_parts = [str(loc) for loc in loc_list]
        loc_str = ".".join(str_parts)

        msg = error_detail.get("msg", "Validation error")
        type_str = error_detail.get("type", "validation_error")

        error_message = (
            f"Failed to process request due to validation error: '{type_str}' at '{loc_str}': {msg}."
        )

    else:
        error_message = f"Validation failed for unknown reason."

    return JSONResponse(
        status_code=status_code,
        content={
            "error": "RequestValidationError",
            "message": error_message
        }
    )