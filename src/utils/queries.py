from typing import Iterable, Union


def interval_query(name: str, interval: Iterable[Union[str, float, int]]) -> dict:
    value_from, value_to = interval
    query = {}

    if isinstance(value_from, float) or isinstance(value_from, int):
        query["$gte"] = value_from

    if isinstance(value_to, float) or isinstance(value_to, int):
        query["$lte"] = value_to

    return {name: query} if query else {}
