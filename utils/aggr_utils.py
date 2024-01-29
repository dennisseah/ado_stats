from typing import Any


def merge(data: list[list[tuple]]) -> list[tuple]:
    """Merges the given data.

    :param data: The data to be merged.
    :return: The merged data.
    """
    base = set()
    for d in data:
        base = base.union(set([x[0] for x in d]))

    dicts = [{x[0]: x[1] for x in d} for d in data]
    results = []
    for dim in base:
        results.append(tuple([dim] + [d.get(dim, 0) for d in dicts]))
    return results


def aggr_count(
    data: list[Any], dimension: str, sort_values=True, include_percentage=False
) -> list[tuple]:
    """Aggregates the given data by the given dimension.

    :param data: The data to be aggregated.
    :param dimension: The dimension to be aggregated.
    :param sort_values: Whether to sort the values.
    :param include_percentage: Whether to include percentage.
    :return: The aggregated data.
    """
    dimensions = set([getattr(d, dimension) for d in data])

    if include_percentage:
        ttl = len(data)
        results = [
            (
                dim,
                len([d for d in data if getattr(d, dimension) == dim]),
                f"""{round(
                    (len([d for d in data if getattr(d, dimension) == dim]) / ttl)
                    * 100,
                    2,
                )}%""",
            )
            for dim in dimensions
            if dim is not None
        ]
    else:
        results = [
            (dim, len([d for d in data if getattr(d, dimension) == dim]))
            for dim in dimensions
            if dim is not None
        ]

    if sort_values:
        results.sort(key=lambda x: x[1])

    return results
