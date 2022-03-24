from pydantic import BaseModel

class ShortenURL(BaseModel):
    short_url:str
    long_url:str
    passphrase:str