from pydantic import BaseModel


class URL(BaseModel):
    new_long_url: str
    passphrase: str