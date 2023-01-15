from django.conf import settings

from utilities.utils import generate_random_string


def generate_short_key() -> str:
    return generate_random_string(settings.MAX_SHORT_KEY_CHARS)
