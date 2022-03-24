from pydantic import BaseModel

class URLUpdate(BaseModel):
    new_long_url: str
    passphrase: str
