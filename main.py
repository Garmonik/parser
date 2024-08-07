from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse

from api.v1.api import api_router as api_v1

app = FastAPI()
app.include_router(api_v1, prefix="")


@app.get("/", deprecated=True)
async def index(req: Request):
    return RedirectResponse(f"{str(req.base_url)[:-1]}{app.docs_url}")
