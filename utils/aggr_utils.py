from typing import Any


def merge(data: list[list[tuple[str, int]]]):
    base = set()
    for d in data:
        base = base.union(set([x[0] for x in d]))

    dicts = []
    for d in data:
        dicts.append({x[0]: x[1] for x in d})

    results = []
    for dim in base:
        results.append(tuple([dim] + [d.get(dim, 0) for d in dicts]))
    return results


def aggr_count(
    data: list[Any], dimension: str, sort_values=True
) -> list[tuple[str, int]]:
    dimensions = set([getattr(d, dimension) for d in data])

    results = [
        (dim, len([d for d in data if getattr(d, dimension) == dim]))
        for dim in dimensions
        if dim is not None
    ]

    if sort_values:
        results.sort(key=lambda x: x[1])

    return results
