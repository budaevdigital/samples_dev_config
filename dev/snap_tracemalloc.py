import tracemalloc
from typing import Any

SNAPSHOTS_TRACE = {}


async def start_trace() -> tuple[bool, str]:
    if not tracemalloc.is_tracing():
        tracemalloc.start()
        return True, "Tracemalloc is started"
    else:
        return False, "Tracemalloc was already started"


async def stop_trace() -> tuple[bool, str]:
    if tracemalloc.is_tracing():
        tracemalloc.stop()
        return True, "Tracemalloc is stopped"
    else:
        return False, "Tracemalloc was not started"


async def take_snap_trace(snapshot_id: str) -> tuple[bool, str]:
    if tracemalloc.is_tracing():
        SNAPSHOTS_TRACE[snapshot_id] = tracemalloc.take_snapshot()
        return True, f"Snapshots {snapshot_id} taken and stored"
    else:
        return False, "Tracemalloc is not running"


async def check_keys_snapshots() -> tuple[bool, list[str]] | tuple[bool, str]:
    if not SNAPSHOTS_TRACE:
        return False, "Snapshots is empty"
    return True, list(SNAPSHOTS_TRACE.keys())


async def get_snapshot(snapshot_id: str, line_count: int | None = None) -> \
        tuple[bool, list[dict[str, Any]]] | tuple[bool, str]:

    if snapshot := SNAPSHOTS_TRACE.get(snapshot_id):
        result = []
        for stat in snapshot.statistics("lineno")[:line_count]:
            result.append({
                "file": str(stat.traceback[0].filename),
                "line": stat.traceback[0].lineno,
                "size": stat.size // 1024,  # Размер в КБ
                "count": stat.count  # Количество выделений памяти
            })
        return True, result
    else:
        return False, f"Snapshot {snapshot_id} is not found"


async def compare_snapshots(snapshot_first: str, snapshot_second: str, line_count: int | None = None) -> \
        tuple[bool, list[dict[str, Any]]] | tuple[bool, str]:

    if not SNAPSHOTS_TRACE.get(snapshot_first) and not SNAPSHOTS_TRACE.get(snapshot_second):
        return True, f"Someone snapshots is not found"

    stats = SNAPSHOTS_TRACE.get(snapshot_second).compare_to(SNAPSHOTS_TRACE.get(snapshot_first), "lineno")
    result = []
    for stat in stats[:line_count]:
        result.append({
            "file": str(stat.traceback[0].filename),
            "line": stat.traceback[0].lineno,
            "size_diff": stat.size_diff // 1024,
            "count_diff": stat.count_diff
        })
    return True, result


async def delete_snapshots(snapshot_id: str | None = None):

    if snapshot_id and SNAPSHOTS_TRACE.get(snapshot_id):
        del SNAPSHOTS_TRACE[snapshot_id]
        return True, f"Snapshot {snapshot_id} was deleted"
    SNAPSHOTS_TRACE.clear()
    return True, "All snapshots was deleted"
