import asyncio

import uvicorn
from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse

from db.database import init_models
from routes.login import loginroute
from routes.referral import referralrouter


app = FastAPI()
app.include_router(loginroute, prefix="/auth")
app.include_router(referralrouter, prefix="/referral")


@app.exception_handler(ValueError)
async def value_error_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": str(exc)},
    )


@app.get("/")
async def index():
    return "Referral "


if __name__ == "__main__":
    asyncio.run(init_models())
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
