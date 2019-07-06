from datetime import datetime
from random import randint

import pytz
from connexion import problem
from flask import after_this_request, request

from throttling_quota import throttle


@throttle
def get_status():
    """Implement the get_status operation
    :return: a problem+json with status 200, title "OK" and a successful
             message in detail
    """
    headers={"Cache-Control": "no-store"}
    
    p = randint(1, 5)
    if p == 5:
        return problem(
            status=503,
            title="Service Temporarily Unavailable",
            detail="Retry after the number of seconds specified in the the Retry-After header.",
            headers={"Retry-After": p, **headers},
        )
    return problem(
        status=200,
        title="OK",
        detail="So far so good.",
        headers=headers,
    )


@throttle
def get_echo(tz="Zulu", user=None, token_info=None):
    if tz not in pytz.all_timezones:
        return problem(
            status=400,
            title="Bad Timezone",
            detail="The specified timezone is not valid",
            ext={"valid_timezones": pytz.all_timezones},
        )
    d = datetime.now(tz=pytz.timezone(tz))
    r = {"timestamp": d.isoformat().replace("+00:00", "Z")}

    #
    # Eventually append user info.
    #
    if user:
        r["user"] = user
        r["ti"] = token_info

    return (r, 200, {})


ALL_TIMEZONES = sorted(pytz.all_timezones)


@throttle
def get_timezones(limit=5, offset=0, continent=None):
    try:
        entries = ALL_TIMEZONES

        if continent is not None:
            continent = str(continent).capitalize() + "/"
            entries = [x for x in entries if x.startswith(continent)]

        entries = entries[offset : offset + limit]
    except IndexError:
        return problem(
            status=404,
            detail=f"No entries between {offset} and {offset + limit}",
            title="Not Found",
        )
    return {
        "limit": limit,
        "offset": offset,
        "entries": entries,
        "count": len(entries),
    }


@throttle
def get_timezone(limit=5, offset=0, continent=None):
    return get_timezones(limit, offset, continent)
