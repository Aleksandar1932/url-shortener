from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from lib.service.url_service import create_short_url, get_long_url, update_short_url
from api.models import URL

app = FastAPI()

@app.get("/{short_url}")
def read_root(short_url: str):
    long_url = get_long_url(short_url)
    if long_url is None:
        return {"error": "Short url not found."}

    return RedirectResponse(long_url)

@app.get("/shorten/")
def shorten(long_url: str):
    short_url, long_url, passphrase = create_short_url(long_url)
    return {"short_url": short_url, "long_url": long_url, "passphrase": passphrase}


@app.post("/update/{short_url}")
def update(short_url, url: URL):

    short_url, long_url = update_short_url(short_url, url.new_long_url, url.passphrase)
    return {"short_url": short_url, "long_url": long_url}