from pydantic import BaseModel


class UpdateURL(BaseModel):
    new_long_url: str
    passphrase: str
