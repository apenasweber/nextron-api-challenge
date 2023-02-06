from fastapi.middleware.cors import CORSMiddleware
from api.routers import expression, login
from fastapi import FastAPI


def get_app() -> FastAPI:
    app = FastAPI()
    app.include_router(login.login_router)
    app.include_router(expression.router)
    return app


app = get_app()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

