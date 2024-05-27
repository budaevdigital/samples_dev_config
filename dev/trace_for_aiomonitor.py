import tracemalloc


def take_snapshot(prev=None, limit=10):
    res = tracemalloc.take_snapshot()
    res = res.filter_traces(
        [
            tracemalloc.Filter(False, tracemalloc.__file__),
        ]
    )

    if prev is None:
        return res

    st = res.compare_to(prev, "lineno")
    for stat in st[:limit]:
        print(stat)

    return res
