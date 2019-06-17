from connexion import problem
from random import randint
import pytz
from datetime import datetime

def get_status():
    """Implement the get_status operation
    :return: a problem+json with status 200, title "OK" and a successful
             message in detail
    """
    p = randint(1, 5)
    if p == 5:
        return problem(
            status=503,
            title="Service Temporarily Unavailable",
            detail="Retry after the number of seconds specified in the the Retry-After header.",
            headers={'Retry-After': p}
        )
    return problem(
        status=200,
        title="OK",
        detail="So far so good."
    )    
    raise NotImplementedError


def get_echo(tz='Zulu'):
    if tz not in pytz.all_timezones:
        return problem(
            status=400,
            title="Bad Timezone",
            detail="The specified timezone is not valid",
            ext={"valid_timezones": pytz.all_timezones}
        )
    d = datetime.now(tz=pytz.timezone(tz))
    return {"timestamp": d.isoformat().replace('+00:00', 'Z')}
