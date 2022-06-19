from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse

from lib.service.url_service import create_short_url, get_long_url, update_short_url
from api.models.request import UpdateURL
from api.models.response import ShortenURL

app = FastAPI(
    title="url-shortener",
    version="0.0.1",
    description="🚀 Simple and extensible URL shortener, which enables editable short URLs.",
    contact={
        "name": "Aleksandar Ivanovski",
        "url": "http://ivanovski.tech",
        "email": "aleksandar.ivanovski123@gmail.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)


@app.get(
    "/{short_url}",
    response_class=RedirectResponse,
    response_description="Redirect to long url.",
)
def read_root(short_url: str):
    """
    Redirect to the long url corresponding to `short_url`.
    """

    try:
        long_url = get_long_url(short_url)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

    return RedirectResponse(long_url)


@app.get("/shorten/", response_model=ShortenURL)
def shorten(long_url: str):
    """
    Shorten the given long url.
    """

    short_url, long_url, passphrase = create_short_url(long_url)
    return ShortenURL(short_url=short_url, long_url=long_url, passphrase=passphrase)


@app.post("/update/{short_url}", response_model=ShortenURL)
def update(short_url, url: UpdateURL):
    """
    Update the long url for a given short url, authorized with the passphrase given while creating the short url.
    """
    try:
        short_url, long_url = update_short_url(
            short_url, url.new_long_url, url.passphrase
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return ShortenURL(short_url=short_url, long_url=long_url, passphrase=url.passphrase)
