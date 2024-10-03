from fastapi import FastAPI, Request
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError
from dotenv import load_dotenv
from starlette.responses import JSONResponse
from routers.index import router
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    secret_key: str = "c4a033c4-1b71-43fc-a7a2-ba1962120fbe"
app = FastAPI()

load_dotenv()

@CsrfProtect.load_config
def get_csrf_config():
    return Settings()


@app.exception_handler(CsrfProtectError)
async def csrf_protect_exception_handler(request: Request, exc: CsrfProtectError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})
@app.middleware("http")
async def csrf_middleware(request: Request, call_next):
    response = await call_next(request)
    if request.method in ("POST", "PUT", "DELETE"):
        csrf_protect = CsrfProtect()
        response.set_cookie(key="csrf_token", value=csrf_protect.generate_csrf_tokens())
    return response


# # basic middleware
# @app.middleware("http")
# async def auth_middleware(request: Request, call_next):
#         if request.url.path != "/api/user/add":
#             if request.headers.get("Authorization") != "Bearer":
#                 return JSONResponse(status_code=401, content={"detail": "Unauthorized"})
#                 return JSONResponse(status_code=401, content={"detail": "Unauthorized"})
#             return  await call_next(request)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
