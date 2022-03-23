import typing

from redis import Redis

from lib.utils.generators import generate_passphrase, generate_short_url

r = Redis(host='localhost', port=6379, db=0, decode_responses=True)

def create_short_url(long_url: str) -> str:
    """
    Shorten a long url.

    Args:
        long_url (str): The long url to shorten.

    Returns:
        str: The shortened url.
        passphrase (str): The passphrase for the shortened url.
    """

    passphrase = generate_passphrase()
    short_url = generate_short_url()

    while short_url in r.keys():
        short_url = generate_short_url()

    r.hmset(short_url, {"long_url": long_url, "passphrase": passphrase})

    return short_url, long_url, passphrase

def get_long_url(short_url: str) -> typing.Optional[str]:
    """
    Get the long url from a short url.

    Args:
        short_url (str): The short url to get the long url for.

    Returns:
        str: The long url.
    """

    long_url = r.hgetall(short_url)
    if long_url == {}:
        return None

    print(long_url)

    return long_url['long_url']

def update_short_url(short_url: str, new_long_url:str, secret: str) -> str:
    """
    Update the long url for a given short url.

    Args:
        short_url (str): The short url to update the long url for.
        new_long_url (str): The new long url.
        secret (str): The secret to update the long url with.

    Returns:
        str: The short url.
    """

    long_url = r.hgetall(short_url)
    if long_url is None:
        raise ValueError("Short url does not exist.")
    
    if long_url['passphrase'] != secret:
        raise ValueError("Invalid secret.")

    r.hmset(short_url, {"long_url": new_long_url, "passphrase": secret})

    return short_url, new_long_url