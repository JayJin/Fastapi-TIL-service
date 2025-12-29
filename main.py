from user.interface.controllers.user_crotroller import router as user_router
import uvicorn

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from containers import Container


app = FastAPI()
app.include_router(user_router)
app.container = Container()
app.container.wire(packages=["user.interface.controllers"])   ### 컨테이너와 패키지 연결 ###

@app.exception_handler(RequestValidationError)      # 예외 핸들러 등록(422 -> 400 변경)
async def validation_exception_handler(
    request: Request, 
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=400,
        content=str(exc.errors()),
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", reload=True)
