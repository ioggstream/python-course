from connexion import problem
from random import randint

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

