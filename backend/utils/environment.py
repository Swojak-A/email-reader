"""Utils for accessing process environment variables"""

import os
from itertools import chain

from django.core.exceptions import ImproperlyConfigured

NOT_SET = object()


def get_env(name: str, expected_type=str, default=NOT_SET):
    try:
        value = os.environ[name]
    except KeyError:
        if default is NOT_SET:
            raise ImproperlyConfigured(
                f"The {name} is not present among environmental variables."
            ) from None
        else:
            return default

    if expected_type == bool:
        return boole_env_mapper(name, value)
    if expected_type == list:
        return list_env_mapper(value)
    return str(value)


def boole_env_mapper(env_name, value: str) -> bool:
    repr_true = ("true", "1", "yes")
    repr_false = ("false", "0", "no")

    if value.lower() in repr_true:
        return True
    if value.lower() in repr_false:
        return False
    raise ImproperlyConfigured(
        f"Value provided in config for {env_name} env var: "
        f"{value} does not map any boolean representations."
        f"Try one of provided values: {chain(repr_true, repr_false)}"
    )


def list_env_mapper(value: str) -> list | str:
    separator = ","

    if value == "":
        return []
    return [str(item.strip()) for item in value.split(separator)]
