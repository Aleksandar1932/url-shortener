from uuid import uuid4

def generate_passphrase():
    return str(uuid4())

def generate_short_url():
    return str(uuid4())[:8]