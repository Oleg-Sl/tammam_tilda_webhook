import sys
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import router as router_api


sys.dont_write_bytecode = True


app = FastAPI(
    title="Tilde form handler",
    version="0.1.0",
    debug=True,
    root_path="/tammam-tilda-webhook",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router_api)


@app.get("/test")
async def test():
    return {"test": 111, 'project_name': "Tilde form handler"}
