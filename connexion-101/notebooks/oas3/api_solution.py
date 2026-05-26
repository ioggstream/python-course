from connexion import AsyncApp
from datetime import datetime
from random import randint
from pathlib import Path
import json

import pytz
from connexion import problem
from starlette.responses import Response
from rfc9530 import OASDigestMiddleware
from decorators.content_digest import content_digest
from decorators.ratelimit import ratelimit


async def get_status():
    """Implement the get_status operation
    :return: a problem+json with status 200, title "OK" and a successful
             message in detail
    """
    headers = {"Cache-Control": "no-store"}

    p = randint(1, 5)
    if p == 5:
        return problem(
            status=503,
            title="Service Temporarily Unavailable",
            detail="Retry after the number of seconds specified in the the Retry-After header.",
            headers={"Retry-After": p, **headers},
        )
    return problem(status=200, title="OK", detail="So far so good.", headers=headers)


@content_digest
async def get_echo(tz="Zulu", user=None, token_info=None):
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

    return r, 200, {"content-type": "application/json"}


ALL_TIMEZONES = sorted(pytz.all_timezones)

@ratelimit(quota=5, ttl=60)
async def get_timezones(limit=5, offset=0, continent=None):
    entries = ALL_TIMEZONES

    if continent is not None:
        continent = str(continent).capitalize() + "/"
        entries = [x for x in entries if x.startswith(continent)]

    entries = entries[offset: offset + limit]
    return {"limit": limit, "offset": offset, "entries": entries, "count": len(entries)}


async def get_timezones_by_continent(limit=5, offset=0, continent=None):
    return get_timezones(limit, offset, continent)


def create_connexion_app(spec: str):
    spec_path = Path(spec)
    app = AsyncApp(
        __name__,
        specification_dir=spec_path.parent.as_posix(),
    )
    app.add_api(
        spec_path.name, validate_responses=True,
    )
    spec_dict = app.middleware.apis[0].specification
    if "solution" in __file__:
        # Patch operationIds so that `api.get_status` and `api.get_echo` resolve to the functions defined in this module.
        for path_item in  spec_dict["paths"].values():
            for operation in path_item.values():
                operation["operationId"] = operation["operationId"].replace("api.", "api_solution.")
    app.add_middleware(OASDigestMiddleware, spec=spec_dict, max_response_size=1000)
    return app


def main(*args, **kwargs):
    import os

    app = create_connexion_app(os.environ["SPEC_FILE"])
    return app
