from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import Request
from urllib.parse import quote

async def custom_validation_exception_handler(request: Request, exc: RequestValidationError):
    status_code = 422
    if exc.errors():
        error_detail = exc.errors()[0]
        print(".".join(error_detail.get("loc",[])))

        loc_str = ".".join(str(loc) for loc in error_detail.get("loc", []))

        msg = error_detail.get("msg", "Validation error")
        type_str = error_detail.get("type", "validation_error")

        encoded_url = quote(str(request.url), safe=':/?&=')

        error_message = (
            f"Failed to process request due to validation error '{type_str}' at '{loc_str}': {msg} "
            f"for url '{encoded_url}'"
        )

    else:
        encoded_url = quote(str(request.url), safe=':/?&=')
        error_message = f"Validation failed for unknown reason at url '{encoded_url}'"

    return JSONResponse(
        status_code=status_code,
        content={
            "error": error_message,
            "status_code": status_code
        }
    )