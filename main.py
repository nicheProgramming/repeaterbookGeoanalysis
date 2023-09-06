from functools import wraps

from dotenv import load_dotenv
from requests_oauthlib import OAuth2Session

import here
import repeaterbook

load_dotenv()


def authenticate(func: callable) -> callable:
    """Decorator to authenticate to the here api before main

    Args:
        func (callable): Takes main as a decorator argument

    Returns:
        wrapper (callable): Returns wrapped main()
    """
    @wraps(func)
    def wrapper():
        # Authenticate to Here
        here_session = here.authenticate()
        func(here_session)

    return wrapper


@authenticate
def main(h_session: OAuth2Session) -> None:
    """Main

    Args:
        h_session (OAuth2Session): Authenticated Here API session
    """
    radius = 10 # in miles

    cities = here.get_cities_in_radius(h_session, radius)

    results = repeaterbook.query_cities(cities)

main()
