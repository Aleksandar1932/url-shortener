def fix_url(url: str) -> str:
    """Fix the url to be a valid url.

    Parameters
    ----------
    url : str
        Url to fix.

    Returns
    -------
    str
        Fixed url (if needed http is appended)
    """

    if not url.startswith("http"):
        url = "http://" + url
    return url
