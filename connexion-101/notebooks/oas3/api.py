def get_status():
    """Implement the get_status operation
    :return: a problem+json with status 200, title "OK" and a successful
             message in detail
    """
    raise NotImplementedError


def get_echo(tz="Zulu", user=None, token_info=None):
    raise NotImplementedError


def get_timezones(limit=5, offset=0, continent=None):
    raise NotImplementedError
    return {"limit": limit, "offset": offset, "entries": entries, "count": len(entries)}


@throttle
def get_timezones_by_continent(limit=5, offset=0, continent=None):
    return get_timezones(limit, offset, continent)
