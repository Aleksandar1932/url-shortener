import typing
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse

from lib.service.url_service import create_short_url, get_long_url, update_short_url
from api.models.request import URLUpdate
from api.models.response import ShortenURL


app = FastAPI()

@app.get("/{short_url}")
def read_root(short_url: str):
    try:
        long_url = get_long_url(short_url)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return RedirectResponse(long_url)

@app.get("/shorten/", response_model=ShortenURL)
def shorten(long_url: str):
    short_url, long_url, passphrase = create_short_url(long_url)
    return ShortenURL(short_url=short_url, long_url=long_url, passphrase=passphrase)

@app.post("/update/{short_url}", response_model=ShortenURL)
def update(short_url, url: URLUpdate):
    try:
        short_url, long_url = update_short_url(short_url, url.new_long_url, url.passphrase)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return ShortenURL(short_url=short_url, long_url=long_url, passphrase=url.passphrase)